# 🏆 Análisis de Usuarios Influyentes

## Descripción
Esta sección detalla el análisis de los 10 usuarios más influyentes en función del conteo de menciones (@).

## Pasos del Proceso
1. **Lectura del Archivo JSON**: Se lee el archivo JSON en un DataFrame de Spark.
2. **Extracción de Menciones**: Se selecciona la columna 'content' y se extraen las menciones utilizando una expresión regular.
3. **Contar Ocurrencias de Menciones**: Se agrupan los datos por mención y se cuenta el número de ocurrencias de cada una.
4. **Obtener Top 10 Usuarios Mencionados**: Se seleccionan los 10 usuarios más mencionados.
5. **Recolectar Resultados**: Se convierte el resultado a una lista de tuplas.
6. **Guardar Resultados**: Se guarda el DataFrame resultante en formato Delta en ADLS.

---

Volver a: [📅 Análisis de Fechas y Usuarios Activos](q1_memory.md) | [😊 Análisis de Emojis Usados](q2_memory.md) | [README](../README.md)
