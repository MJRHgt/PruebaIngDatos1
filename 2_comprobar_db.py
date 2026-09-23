import sqlite3
import pandas as pd

# Conectar a la base de datos recién creada
conexion = sqlite3.connect('base_prueba.db')

print("="*60)
print("1. CANTIDAD DE REGISTROS POR TABLA")
print("="*60)

tablas = ['CarteraClientes', 'ClientesActualizado', 'TransaccionesActualizado']

for tabla in tablas:
    query_count = f"SELECT COUNT(*) AS TotalRegistros FROM {tabla};"
    total = pd.read_sql_query(query_count, conexion).iloc[0]['TotalRegistros']
    print(f"Tabla '{tabla}': {total} registros")

print("\n" + "="*60)
print("2. PRIMEROS 3 REGISTROS DE CarteraClientes")
print("="*60)
df_cartera = pd.read_sql_query("SELECT * FROM CarteraClientes LIMIT 3;", conexion)
print(df_cartera.to_string(index=False))

print("\n" + "="*60)
print("3. PRIMEROS 3 REGISTROS DE ClientesActualizado")
print("="*60)
df_clientes = pd.read_sql_query("SELECT * FROM ClientesActualizado LIMIT 3;", conexion)
print(df_clientes.to_string(index=False))

print("\n" + "="*60)
print("4. PRIMEROS 3 REGISTROS DE TransaccionesActualizado")
print("="*60)
df_transacciones = pd.read_sql_query("SELECT * FROM TransaccionesActualizado LIMIT 3;", conexion)
print(df_transacciones.to_string(index=False))

conexion.close()