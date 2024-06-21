# 📅 Análisis de Fechas y Usuarios Activos

## Descripción
Esta sección detalla el análisis de las 10 fechas con la mayor cantidad de tweets y los usuarios más activos en cada una de esas fechas.

## Pasos del Proceso
1. **Lectura del Archivo JSON**: Se lee el archivo JSON en un DataFrame de Spark.
2. **Selección y Transformación de Datos**: Se seleccionan las columnas necesarias y se convierte la columna de fecha al tipo de dato `date`.
3. **Contar Tweets por Fecha**: Se agrupan los datos por fecha y se cuenta el número de tweets para cada fecha.
4. **Contar Tweets por Usuario por Fecha**: Se obtiene el usuario con más tweets para cada fecha.
5. **Unir DataFrames**: Se unen los DataFrames de tweets por fecha y tweets por usuario por fecha.
6. **Recolectar Resultados**: Se convierte el resultado a una lista de tuplas.
7. **Guardar Resultados**: Se guarda el DataFrame resultante en formato Delta en ADLS.

---

Volver a: [😊 Análisis de Emojis Usados](q2_memory.md) | [🏆 Análisis de Usuarios Influyentes](q3_memory.md) | [README](../README.md)
