import sqlite3
import pandas as pd

# Conectar a la base de datos local
conexion = sqlite3.connect('base_prueba.db')

# Define aquí la consulta que deseas ejecutar
query_pregunta_1 = """
SELECT COUNT(*) AS TotalClientes FROM CarteraClientes;
"""

# Ejecutar y mostrar resultado
resultado = pd.read_sql_query(query_pregunta_1, conexion)
print(resultado.to_string(index=False))

conexion.close()