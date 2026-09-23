import sqlite3
import pandas as pd

# Conectar a la base de datos local
conexion = sqlite3.connect('base_prueba.db')

#1 ejercicio
query_1 = """

--Crear una Tabla temporal, para hacer calculo por soporte de SQL LITE
WITH TotalesSucursal AS (
    SELECT 
        Sucursal,
        SUM(Monto) AS GranTotalSucursal
    FROM CarteraClientes
    GROUP BY Sucursal
)
SELECT 
    c.Sucursal,
    c.EtapaCredito,
    COUNT(DISTINCT c.ClienteID) AS TotalClientesUnicos,
    SUM(c.Monto) AS MontoTotal,
    ROUND(AVG(c.Monto), 2) AS MontoPromedio,
    ROUND(AVG(c.DiasAtraso), 2) AS PromedioDiasAtraso,
    --ROUND(SQRT(AVG(c.Monto * c.Monto) - (AVG(c.Monto) * AVG(c.Monto))), 2) AS DesviacionEstandarMonto, -- SQL Lite no me soporto Raiz, dejo constancia
    ROUND((SUM(c.Monto) * 100.0) / t.GranTotalSucursal, 2) AS PorcentajeMontoSucursal
FROM CarteraClientes c
JOIN TotalesSucursal t ON c.Sucursal = t.Sucursal
GROUP BY c.Sucursal, c.EtapaCredito;

"""
df_q1 = pd.read_sql_query(query_1, conexion)
print(df_q1.to_string(index=False))


#2 ejercicio
query_2 = """


SELECT cc.Sucursal, cc.EtapaCredito
FROM CarteraClientes cc
limit 3

"""
df_q2 = pd.read_sql_query(query_2, conexion)
print(df_q2.to_string(index=False))

'''
#3 ejercicio
query_3 = """


SELECT cc.Sucursal, cc.EtapaCredito
FROM CarteraClientes cc
limit 3

"""
df_q3_res = pd.read_sql_query(query_3, conexion)
print(df_q3_res.to_string(index=False))

#4 ejercicio
query_4 = """


SELECT cc.Sucursal, cc.EtapaCredito
FROM CarteraClientes cc
limit 3

"""
df_q4 = pd.read_sql_query(query_4, conexion)
print(df_q4.to_string(index=False))

'''
conexion.close()