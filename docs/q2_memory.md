# 😊 Análisis de Emojis Usados

## Descripción
Esta sección detalla el análisis de los 10 emojis más usados y su respectivo conteo.

## Pasos del Proceso
1. **Lectura del Archivo JSON**: Se lee el archivo JSON en un DataFrame de Spark.
2. **Extracción de Emojis**: Se selecciona la columna 'content' y se extraen los emojis utilizando una expresión regular.
3. **Contar Ocurrencias de Emojis**: Se agrupan los datos por emoji y se cuenta el número de ocurrencias de cada uno.
4. **Obtener Top 10 Emojis**: Se seleccionan los 10 emojis más usados.
5. **Recolectar Resultados**: Se convierte el resultado a una lista de tuplas.
6. **Guardar Resultados**: Se guarda el DataFrame resultante en formato Delta en ADLS.

---

Volver a: [📅 Análisis de Fechas y Usuarios Activos](q1_memory.md) | [🏆 Análisis de Usuarios Influyentes](q3_memory.md) | [README](../README.md)
