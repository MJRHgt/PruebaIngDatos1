import sqlite3
import pandas as pd

# Conectar a la base de datos local
conexion = sqlite3.connect('base_prueba.db')

print("---> Ejecutando Query 1")
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
df_q1.to_csv('1_Query.csv', index=False)

print("\n---> Ejecutando Query 2")
#2 ejercicio
query_2 = """


SELECT 
    ClienteID,
    NombreCliente,
    SegmentoEdad AS EdadEstimada,
    Monto,
    EtapaCredito,
    DiasAtraso
FROM CarteraClientes
--Se soluciona tema de 2 o mas, con case para ir sumando
WHERE (
    (CASE WHEN DiasAtraso > 60 THEN 1 ELSE 0 END) + -- dias de atraso
    (CASE WHEN EtapaCredito IN ('61_90D', '31_60D') THEN 1 ELSE 0 END) + --segmento de mora o etapa de credio
    (CASE WHEN SegmentoEdad = '18-25' THEN 1 ELSE 0 END) -- segmento de edad
) >= 2 --validacion de 2 o mas
--limit 3 --verificacion; con id 9 y 13 cumplen
;
"""
df_q2 = pd.read_sql_query(query_2, conexion)
print(df_q2.to_string(index=False))
df_q2.to_csv('2_Query.csv', index=False)

print("\n---> Ejecutando Query 3")

#3 ejercicio
query_3 = """


--SELECT ClienteID, 'Monto menor o igual a 0' AS TipoError FROM CarteraClientes WHERE Monto <= 0 LIMIT 3;-- No hay
--SELECT ClienteID, 'Días de atraso negativo' AS TipoError FROM CarteraClientes WHERE DiasAtraso < 0 LIMIT 3;-- Confirmo 35 y 40 ID
--SELECT ClienteID, 'Fecha actualización futura' AS TipoError FROM CarteraClientes WHERE UltimaActualizacion > CURRENT_TIMESTAMP LIMIT 3;-- no hay

WITH Inconsistencias AS (
    SELECT ClienteID, 'Monto menor o igual a 0' AS TipoError 
    FROM CarteraClientes 
    WHERE Monto <= 0
    
    UNION ALL
    
    SELECT ClienteID, 'Días de atraso negativo' AS TipoError 
    FROM CarteraClientes 
    WHERE DiasAtraso < 0
    
    UNION ALL
    
    SELECT ClienteID, 'Fecha actualización futura' AS TipoError 
    FROM CarteraClientes 
    WHERE UltimaActualizacion > CURRENT_TIMESTAMP
)
SELECT 
    TipoError, 
    COUNT(ClienteID) AS Cantidad
FROM Inconsistencias
GROUP BY TipoError;


"""
df_q3 = pd.read_sql_query(query_3, conexion)
print(df_q3.to_string(index=False))
df_q3.to_csv('3_Query.csv', index=False)


print("\n---> Ejecutando Query 4")
#4 ejercicio

query_4 = """

WITH TotalesSucursal AS (
    SELECT 
        Sucursal,
        COUNT(DISTINCT ClienteID) AS TotalClientesSucursal
    FROM CarteraClientes
    GROUP BY Sucursal
)
SELECT 
    c.Sucursal,
    c.SegmentoEdad,
    c.Sexo,
    COUNT(DISTINCT c.ClienteID) AS TotalClientes,
    ROUND(AVG(c.Monto), 2) AS MontoPromedio,
    ROUND((COUNT(DISTINCT c.ClienteID) * 100.0) / t.TotalClientesSucursal, 2) AS PorcentajeClientesSucursal
FROM CarteraClientes c
JOIN TotalesSucursal t ON c.Sucursal = t.Sucursal
GROUP BY c.Sucursal, c.SegmentoEdad, c.Sexo;
--Se podria crear un cursor

"""
df_q4 = pd.read_sql_query(query_4, conexion)
print(df_q4.to_string(index=False))
df_q4.to_csv('4_Query.csv', index=False)

print("\n---> Ejecutando Query Bonus")

query_5 = """ 

WITH ClasificacionRiesgo AS (
    SELECT 
        ClienteID,
        Sucursal,
        Monto,
        --REgla de riesgos
        CASE 
            WHEN DiasAtraso > 60 OR EtapaCredito = '61_90D' THEN 'Alta'
            WHEN EtapaCredito IN ('31_60D', '1_30D') THEN 'Media'
            WHEN EtapaCredito = '0SANA' THEN 'Baja'
            ELSE 'Desconocido'
        END AS NivelRiesgo
    FROM CarteraClientes
)
SELECT 
    Sucursal,
    NivelRiesgo,
    COUNT(ClienteID) AS TotalClientes,
    SUM(Monto) AS MontoTotal
    --,
    --DENSE_RANK() OVER (PARTITION BY Sucursal ORDER BY COUNT(ClienteID) DESC) AS RankingRiesgoEnSucursal 
    -- Rank complicado particionando por #clientes; no me ha funcionado supongo por la versi´on de SQL
FROM ClasificacionRiesgo
GROUP BY Sucursal, NivelRiesgo;

"""
df_q5 = pd.read_sql_query(query_5, conexion)
print(df_q5.to_string(index=False))
df_q5.to_csv('5_Query.csv', index=False)

conexion.close() #cerrar conexion
print("\nProceso finalizado. Todos los archivos CSV están listos.")