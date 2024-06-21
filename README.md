<!-- Logo de LATAM -->
<p align="center">
  <img src="https://pressreleasecom.wordpress.com/wp-content/uploads/2017/06/pressrelease-logo-latam-airlines.jpg" width="300">
</p>

<!-- Título del Proyecto -->
<h1 align="center" style="color: #A01F30;">Documentación del Proyecto de Análisis de Tweets</h1>

<!-- Descripción General -->
<p align="center" style="color: #003366; font-size: 18px;">
  Bienvenido a la documentación del proyecto de análisis de tweets. Este proyecto utiliza PySpark para procesar y analizar un archivo JSON de tweets almacenado en Azure Data Lake Storage (ADLS).
</p>

<!-- Detalles del Proyecto -->
## Descripción del Proyecto

Este proyecto se enfoca en el análisis de datos de tweets para obtener insights valiosos. Los principales objetivos del proyecto son:

1. 📅 Identificar las 10 fechas con la mayor cantidad de tweets y el usuario más activo en cada una de esas fechas.
2. 😊 Encontrar los 10 emojis más usados y su respectivo conteo.
3. 🏆 Determinar los 10 usuarios más influyentes en función del conteo de menciones (@).

## Pasos del Proceso

### 1. Inicialización y Configuración
- Definir las rutas base para los archivos de datos, de salida y de logs.
- Crear los directorios de salida y logs si no existen.
- Configurar un logger personalizado para registrar mensajes en un archivo de texto.

### 2. Ejecución del Análisis
Cada uno de los análisis se realiza a través de funciones específicas, optimizadas para el uso eficiente del tiempo y la memoria.

- **[📅 Análisis de Fechas y Usuarios Activos](docs/q1_memory.md)**
- **[😊 Análisis de Emojis Usados](docs/q2_memory.md)**
- **[🏆 Análisis de Usuarios Influyentes](docs/q3_memory.md)**

### 3. Resultados y Logs
- Los resultados se guardan en formato Delta en ADLS.
- Los detalles de la ejecución se registran en un archivo de log para referencia futura.

### Cosas que se asumen

1. **Ingesta de Datos**:
   - La data fue previamente ingestada desde Google Drive hacia Azure Data Lake. Esto se debe a que el antivirus de Google Drive impide usar un conector o importar mediante un trigger la data. En cualquier otro caso, se podría conectar a una fuente externa como una base de datos o mediante algún API.

2. **Procesamiento por Lotes (Batch)**:
   - El procesamiento se realiza en lotes (batch) y la data se consulta en la ruta del datalake:
     ```markdown
     https://rawlatamdata.blob.core.windows.net/rawdata/tweets.json.zip
     ```
     Luego, se descomprime en formato JSON en:
     ```markdown
     https://rawlatamdata.blob.core.windows.net/processeddata/farmers-protest-tweets-2021-2-4.json
     ```

3. **Ejecución Manual del Pipeline**:
   - El pipeline de ingesta se ejecuta manualmente, leyendo el archivo almacenado en el Data Lake. Asumiendo que esta parte fuese automatizada, se podría establecer un trigger periódico para traer la data desde una fuente externa con cada ejecución. Sin embargo, el ejercicio actual no lo requiere.

4. **Cluster Interactivo para Procesamiento**:
   - Para el procesamiento de la información y los cálculos, se utilizó Databricks con un clúster interactivo. Este clúster puede ser reemplazado por un job cluster o un pool de instancias para reducir costos. No obstante, para este ejercicio, se utiliza un clúster interactivo por facilidad de uso y demostración.

   **Configuración del Clúster**:
   - **Cluster ID**: `0619-233222-rjlnjfll`
   - **Usuario Creador**: `juan.afanador24@hotmail.com`
   - **Tipo de Nodo**: `Standard_DS3_v2`
   - **Versión de Spark**: `15.2.x-scala2.12`
   - **Máximo de Núcleos**: `4`
   - **Memoria Total**: `14.3 GB`
   - **Tiempo de Autoterminado**: `30 minutos`
   - **Tipo de Disponibilidad**: `ON_DEMAND_AZURE`

5. **Seguridad y Almacenamiento de Credenciales**:
   - Para proteger credenciales y mantener la consistencia de las rutas, se optó por almacenar datos sensibles en Azure Key Vault junto con Unity Catalog.

# Guía Paso a Paso del Proceso de Orquestación

## Pipeline de Orquestación en Azure Data Factory

### Descripción General

Este proceso de orquestación está diseñado para gestionar la ingesta, el procesamiento y la transformación de datos de tweets almacenados en Azure Data Lake Storage (ADLS). La orquestación se divide en dos pipelines principales: `Raw_ingestion` para la ingesta de datos en bruto y `Refined_ingestion` para el procesamiento y análisis de datos refinados.

### Pasos del Proceso

1. **Pipeline de Orquestación Principal**

    El pipeline principal, llamado `Orchestration`, orquesta la ejecución de dos pipelines subordinados:
    
    - **Bronze**: Ejecuta el pipeline `Raw_ingestion`.
    - **Silver**: Ejecuta el pipeline `Refined_ingestion` después de la finalización exitosa del pipeline `Raw_ingestion`.

2. **Pipeline de Ingesta Bruta (Raw_ingestion)**

    Este pipeline se encarga de leer los datos en formato ZIP desde Azure Data Lake, descomprimirlos y almacenarlos en formato JSON en una ubicación específica en el Data Lake.
    
    - **Actividad de Ingesta de Datos**: Se configura una actividad de copia que lee los archivos ZIP desde el Data Lake, los descomprime y los almacena en formato JSON. La configuración incluye detalles sobre la fuente (Azure Blob Storage), el destino (Azure Blob Storage) y las configuraciones de formato de archivo.

3. **Pipeline de Ingesta Refinada (Refined_ingestion)**

    Este pipeline se encarga de ejecutar una serie de notebooks de Databricks que realizan diferentes cálculos y transformaciones en los datos. Cada notebook está diseñado para un propósito específico de procesamiento y análisis.

    #### Actividades en `Refined_ingestion`:

    - **q1_memory**: 
        - Calcula las 10 fechas con la mayor cantidad de tweets.
        - Identifica el usuario con más tweets en cada una de esas fechas.
        - Optimiza el uso de memoria durante el procesamiento.
    
    - **q1_time**:
        - Calcula las 10 fechas con la mayor cantidad de tweets.
        - Identifica el usuario con más tweets en cada una de esas fechas.
        - Optimiza el tiempo de ejecución del proceso.
    
    - **q2_memory**:
        - Calcula los 10 emojis más usados y su conteo.
        - Optimiza el uso de memoria durante el procesamiento.
    
    - **q2_time**:
        - Calcula los 10 emojis más usados y su conteo.
        - Optimiza el tiempo de ejecución del proceso.
    
    - **q3_memory**:
        - Calcula los 10 usuarios más influyentes en función del conteo de menciones.
        - Optimiza el uso de memoria durante el procesamiento.
    
    - **q3_time**:
        - Calcula los 10 usuarios más influyentes en función del conteo de menciones.
        - Optimiza el tiempo de ejecución del proceso.

    Cada una de estas actividades está configurada para ejecutarse de manera secuencial o en paralelo, dependiendo de las dependencias definidas. Cada notebook recibe como parámetro la ruta del archivo JSON en el Data Lake y ejecuta sus respectivas tareas de procesamiento.



## Posibles Optimizaciones Futuras

- **Optimización de Particiones**: Ajustar el número de particiones basadas en el tamaño del dataset para mejorar el paralelismo y el rendimiento.
- **Uso de `broadcast` para DataFrames Pequeños**: Utilizar la función `broadcast` de Spark para DataFrames pequeños que se unen frecuentemente, para optimizar el tiempo de unión.
- **Manejo Avanzado de Errores**: Implementar estrategias de reintento y manejo de errores más detalladas para mejorar la robustez del proceso.
- **Escalado Automático**: Configurar el escalado automático del clúster de Databricks para manejar dinámicamente cargas de trabajo variables y optimizar el costo.
- **Profiling de Código**: Realizar un profiling detallado del código utilizando herramientas como `PySpark Profiler` para identificar y optimizar partes específicas del código que consumen más recursos.

---

<p align="center" style="color: #A01F30;">
  Proyecto realizado por Juan José Afanador
</p>
