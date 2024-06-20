# Databricks notebook source
# MAGIC %md
# MAGIC # **Documentación del Código**
# MAGIC
# MAGIC ## **Descripción General**
# MAGIC Este script de PySpark se utiliza para procesar y analizar un archivo JSON de tweets almacenado en Azure Data Lake Storage (ADLS). El objetivo principal es encontrar los 10 usuarios más influyentes en función del conteo de las menciones (@) que registran cada uno de ellos. El resultado se guarda en formato Delta en ADLS, y se registran los detalles de la ejecución en un archivo de log. Esta versión del código se enfoca en optimizar el uso de memoria.
# MAGIC
# MAGIC ## **Pasos del Proceso**
# MAGIC
# MAGIC 1. **Inicialización y Configuración**:
# MAGIC     - Se definen las rutas base para los archivos de datos, de salida y de logs.
# MAGIC     - Se crean los directorios de salida y logs si no existen.
# MAGIC     - Se configura un logger personalizado para registrar mensajes en un archivo de texto.
# MAGIC
# MAGIC 2. **Función `q3_memory`**:
# MAGIC     - **Entrada**: La función recibe la ruta del archivo JSON que contiene los datos de los tweets.
# MAGIC     - **Salida**: Devuelve una lista de tuplas con los 10 usuarios más mencionados y su respectivo conteo.
# MAGIC
# MAGIC 3. **Ejecución del Proceso**:
# MAGIC     - **Inicio del Temporizador y Medición de Memoria**:
# MAGIC         - Se inicia el temporizador y se mide el uso de memoria antes de comenzar el procesamiento.
# MAGIC         - Se registra el inicio de la ejecución de la función.
# MAGIC
# MAGIC     - **Lectura del Archivo JSON**:
# MAGIC         - Se lee el archivo JSON en un DataFrame de Spark.
# MAGIC         - Se registra el tiempo y el uso de memoria después de leer el archivo JSON.
# MAGIC
# MAGIC     - **Selección y Extracción de Menciones**:
# MAGIC         - Se selecciona la columna `content` de los tweets.
# MAGIC         - Se define una función UDF (`extract_mentions_udf`) para extraer las menciones del texto de los tweets.
# MAGIC         - Se aplica la función UDF para extraer las menciones y se explota el resultado en nuevas filas.
# MAGIC         - Se registra el tiempo y el uso de memoria después de la extracción de menciones.
# MAGIC
# MAGIC     - **Contar Menciones**:
# MAGIC         - Se agrupan los datos por mención y se cuenta el número de ocurrencias de cada mención.
# MAGIC         - Se ordenan las menciones por el conteo en orden descendente.
# MAGIC         - Se obtiene el top 10 de las menciones más frecuentes.
# MAGIC         - Se registra el tiempo y el uso de memoria después del conteo de menciones.
# MAGIC
# MAGIC     - **Recolectar Resultados**:
# MAGIC         - Se convierte el resultado a una lista de tuplas.
# MAGIC         - Se registra el tiempo y el uso de memoria después de recolectar los resultados.
# MAGIC
# MAGIC     - **Calcular Tiempos y Memoria Total**:
# MAGIC         - Se calculan y registran los tiempos y uso de memoria total durante el proceso.
# MAGIC
# MAGIC     - **Guardar Resultados**:
# MAGIC         - Se guarda el DataFrame resultante en formato Delta en ADLS.
# MAGIC         - Se registra el guardado del resultado en formato Delta.
# MAGIC
# MAGIC     - **Guardar Logs**:
# MAGIC         - Se guarda el contenido de los logs en un archivo de texto en ADLS.
# MAGIC         - Se registra el guardado de los logs.
# MAGIC
# MAGIC 4. **Manejo de Excepciones**:
# MAGIC     - En caso de errores durante la ejecución, se registran los errores y se guardan los logs antes de finalizar la función.
# MAGIC
# MAGIC ## **Optimizaciones Realizadas**
# MAGIC
# MAGIC - **Extracción de Menciones con UDF**:
# MAGIC     - Se utiliza una función definida por el usuario (UDF) para extraer las menciones del texto de los tweets, asegurando una extracción eficiente y precisa.
# MAGIC - **Cacheo Estratégico**:
# MAGIC     - Se evitó el uso innecesario de `.cache()` para reducir el uso de memoria.
# MAGIC     - Solo se seleccionaron las columnas necesarias para reducir el tamaño del DataFrame en memoria.
# MAGIC - **Uso Eficiente de Funciones de Spark**:
# MAGIC     - Se aseguraron transformaciones eficientes utilizando funciones de Spark SQL, eliminando operaciones redundantes.
# MAGIC - **Monitoreo de Memoria y Tiempos**:
# MAGIC     - Se implementó el monitoreo de uso de memoria y tiempos de ejecución en cada etapa del proceso para identificar y optimizar cuellos de botella.
# MAGIC
# MAGIC ## **Posibles Optimizaciones Futuras**
# MAGIC
# MAGIC - **Optimización de Particiones**:
# MAGIC     - Ajustar el número de particiones basadas en el tamaño del dataset para mejorar el paralelismo y el rendimiento.
# MAGIC - **Uso de `broadcast` para DataFrames Pequeños**:
# MAGIC     - Utilizar la función `broadcast` de Spark para DataFrames pequeños que se unen frecuentemente, para optimizar el tiempo de unión.
# MAGIC - **Manejo Avanzado de Errores**:
# MAGIC     - Implementar estrategias de reintento y manejo de errores más detalladas para mejorar la robustez del proceso.
# MAGIC - **Escalado Automático**:
# MAGIC     - Configurar el escalado automático del clúster de Databricks para manejar dinámicamente cargas de trabajo variables y optimizar el costo.
# MAGIC - **Profiling de Código**:
# MAGIC     - Realizar un profiling detallado del código utilizando herramientas como `PySpark Profiler` para identificar y optimizar partes específicas del código que consumen más recursos.
# MAGIC
# MAGIC

# COMMAND ----------

dbutils.widgets.text("path", "")
file_path = dbutils.widgets.get("path")

# COMMAND ----------

import time
import psutil
import logging
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, ArrayType
from datetime import datetime
from typing import List, Tuple
import os
import re

# Extraer la ruta base del archivo de datos y crear los directorios de output y logs
base_path = os.path.dirname(file_path)
output_directory = os.path.join(base_path, "output")
log_directory = os.path.join(base_path, "logs")
output_file_path = os.path.join(output_directory, "q3_memory_result")
log_file_path = os.path.join(log_directory, "q3_memory_log.txt")

# Crear los directorios para los resultados y logs si no existen
dbutils.fs.mkdirs(output_directory)
dbutils.fs.mkdirs(log_directory)

# Configurar el logger para escribir en un archivo de texto
log_messages = []

def log(message: str):
    """Agrega un mensaje al log y lo imprime."""
    log_messages.append(message)
    print(message)

def save_log_to_file(log_file_path: str):
    """Guarda los mensajes de log en un archivo en ADLS."""
    log_content = "\n".join(log_messages)
    dbutils.fs.put(log_file_path, log_content, overwrite=True)

def get_memory_usage():
    """Obtiene el uso de memoria actual en MB."""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024

def extract_mentions(text):
    """Extrae todas las menciones de un texto."""
    mention_pattern = re.compile(r'@\w+')
    return mention_pattern.findall(text)

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Esta función calcula los 10 usuarios más influyentes en función del conteo de las menciones, optimizando el uso de memoria.

    Args:
    - file_path (str): La ruta al archivo JSON que contiene los datos de los tweets.

    Returns:
    - List[Tuple[str, int]]: Una lista de tuplas donde cada tupla contiene un nombre de usuario y su conteo de menciones.
    """
    try:
        # Iniciar el temporizador
        start_time = time.time()
        start_memory = get_memory_usage()
        log("Inicio de la ejecución de q3_memory")
        
        # Leer el archivo JSON en un DataFrame
        log("Leyendo el archivo JSON...")
        df = spark.read.json(file_path)
        read_time = time.time()
        read_memory = get_memory_usage()
        log(f"Tiempo para leer el JSON: {round(read_time - start_time, 2)} segundos")
        log(f"Uso de memoria después de leer el JSON: {round(read_memory - start_memory, 2)} MB")
        
        # Seleccionar la columna 'content' y extraer las menciones
        log("Extrayendo menciones de los tweets...")
        extract_mentions_udf = F.udf(extract_mentions, ArrayType(StringType()))
        df_mentions = df.withColumn("mentions", F.explode(extract_mentions_udf(F.col("content"))))
        
        # Contar el número de ocurrencias de cada mención
        mention_counts = df_mentions.groupBy("mentions").count().orderBy(F.desc("count"))
        
        # Obtener los 10 usuarios más mencionados
        top_10_mentions = mention_counts.limit(10)
        
        # Convertir el resultado a una lista de tuplas
        log("Recolectando resultados...")
        result = [(row["mentions"], row["count"]) for row in top_10_mentions.collect()]
        collect_time = time.time()
        collect_memory = get_memory_usage()
        log(f"Tiempo para recolectar resultados: {round(collect_time - start_time, 2)} segundos")
        log(f"Uso de memoria después de recolectar resultados: {round(collect_memory - start_memory, 2)} MB")
        
        # Calcular el tiempo total tomado para el proceso
        total_time = collect_time - start_time
        total_memory = collect_memory - start_memory
        log(f"Tiempo total: {round(total_time, 2)} segundos")
        log(f"Uso total de memoria: {round(total_memory, 2)} MB")
        
        # Guardar el resultado en un archivo Delta en la misma ruta del Unity Catalog
        result_df = spark.createDataFrame(result, schema=["username", "count"])
        result_df.write.format("delta").mode("overwrite").save(output_file_path)
        log(f"Resultado guardado en formato Delta en: {output_file_path}")
        
        # Guardar los logs en un archivo
        save_log_to_file(log_file_path)
        log(f"Logs guardados en: {log_file_path}")
        
        return result
    
    except Exception as e:
        log(f"Error durante la ejecución de q3_memory: {e}")
        print(f"Error durante la ejecución de q3_memory: {e}")
        # Guardar los logs en caso de error
        save_log_to_file(log_file_path)
        return []

# Ejemplo de uso
try:
    top_10_mentions = q3_memory(file_path)
    print(top_10_mentions)
    # Almacenar el resultado final en una variable
    final_result = top_10_mentions
except Exception as e:
    print(f"Error al ejecutar la función principal: {e}")




# COMMAND ----------


