import pandas as pd
import sqlite3

print("Iniciando proceso ETL (Ejercicio2)...")

#Archivos de entrada
df_clientes = pd.read_csv('clientes_actualizado.csv')
df_transacciones = pd.read_csv('transacciones_actualizado.csv')

#Transformar campo a:
df_transacciones['FechaPago'] = pd.to_datetime(df_transacciones['FechaPago'])

#Calculos
df_agrupado = df_transacciones.groupby('ClienteID').agg(
    MontoPagado=('MontoPagado', 'sum'),
    PagosTotales=('ClienteID', 'count'),
    FechaUltimoPago=('FechaPago', 'max')
).reset_index()

#Asegurar campo transformado
df_agrupado['FechaUltimoPago'] = df_agrupado['FechaUltimoPago'].dt.strftime('%Y-%m-%d')

#unir tablas
df_leftJoin = pd.merge(df_clientes, df_agrupado, on='ClienteID', how='left')

#Tranformacion si es null se va a 0
df_leftJoin['MontoPagado'] = df_leftJoin['MontoPagado'].fillna(0)
df_leftJoin['PagosTotales'] = df_leftJoin['PagosTotales'].fillna(0).astype(int)

#Estado con regla de negocio, no contepla error
df_leftJoin['EstadoPago'] = df_leftJoin.apply(
    lambda fila: 'Al día' if fila['MontoPagado'] >= fila['MontoOriginal'] else 'En mora', 
    axis=1
)

#yabla final 
columnas_finales = [
    'ClienteID', 'Nombre', 'MontoOriginal', 'MontoPagado', 
    'PagosTotales', 'FechaUltimoPago', 'EstadoPago'
]
df_final = df_leftJoin[columnas_finales]

#Revision
print("\nVista previa de la tabla transformada:")
print(df_final.head().to_string(index=False))

#Carga de Datos
archivo_salida = 'Resultado_ETL_Clientes.csv'
df_final.to_csv(archivo_salida, index=False)
print(f"\nArchivo exportado exitosamente: {archivo_salida}")

print("\nCreando base_prueba_v2.db con las 4 tablas...")
conexion = sqlite3.connect('base_prueba_v2.db')

#Nueva tabla en V2 de base de datos, para saber o insertar en un motor real, no pude en local, para no modificar la v1, pese a usar git
df_final.to_sql('ClientesTransformado', conexion, if_exists='replace', index=False)

conexion.close()
print("Base de datos 'base_prueba_v2.db' ")