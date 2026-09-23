import sqlite3 #base_Local
import pandas as pd
#ejecutado con python 1_crear_tablas.py en terminal de VC
# 1. Conectar a la base de datos local
conexion = sqlite3.connect('base_prueba.db')
cursor = conexion.cursor()

print("-> Leyendo archivos CSV...")
df_cartera = pd.read_csv('cartera_clientes.csv')
df_clientes = pd.read_csv('clientes_actualizado.csv')
df_transacciones = pd.read_csv('transacciones_actualizado.csv')

# 3. Formatear fechas de la cartera para evitar inconsistencias en consultas SQL
if 'FechaDesembolso' in df_cartera.columns:
    df_cartera['FechaDesembolso'] = pd.to_datetime(df_cartera['FechaDesembolso']).dt.strftime('%Y-%m-%d')

if 'UltimaActualizacion' in df_cartera.columns:
    df_cartera['UltimaActualizacion'] = pd.to_datetime(df_cartera['UltimaActualizacion']).dt.strftime('%Y-%m-%d %H:%M:%S')

# 4. Insertar DataFrames en SQLite
df_cartera.to_sql('CarteraClientes', conexion, if_exists='replace', index=False)
df_clientes.to_sql('ClientesActualizado', conexion, if_exists='replace', index=False)
df_transacciones.to_sql('TransaccionesActualizado', conexion, if_exists='replace', index=False)

print("¡Base de datos y tablas creadas exitosamente!")

# 5. Confirmar las tablas creadas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()
print(f"Tablas registradas en base_prueba.db: {[t[0] for t in tablas]}")

conexion.close()