#!/usr/bin/python3
import numpy
import os
import sys
from google.cloud import bigquery
query = """INSERT INTO datosTest.TABLA_UNIFICADA
SELECT * from  datosTest.stage_IGTV8;"""
#query2 = "DROP TABLE datosTest.IGTV_PRODUCCION"
query3 = """INSERT INTO datosTest.IGTV_PRODUCCION  
SELECT A.canal,A.fecha_carga,A.fecha_creacion,A.url,A.titulo,A.comentario,A.likes,A.likes-B.likes dife_likes,A.reproducciones,A.reproducciones-B.reproducciones dife_repro,A.comentarios,A.comentarios-B.comentarios dife_coment
FROM (SELECT * from   datosTest.TABLA_UNIFICADA where fecha_carga=(SELECT max(fecha_carga) from datosTest.TABLA_UNIFICADA)) A
LEFT JOIN (SELECT * from datosTest.TABLA_UNIFICADA  where fecha_carga=(SELECT DATE_SUB(max(fecha_carga), INTERVAL 1 DAY) from datosTest.TABLA_UNIFICADA)) B
ON A.url=B.url;"""
dataset_id = 'datosTest'
#table_id = 'stage_IGTV8'
SERVICE_ACCOUNT_CREDENTIALS_FILE="/IGTV/warehouse.json"
PROJECT_ID="warehouse-245019"
bigquery_client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_CREDENTIALS_FILE, project=PROJECT_ID)


query_job = bigquery_client.query(query)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.name)
print("se cargo stage en unificada")
#query_job = bigquery_client.query(query2)  # API request
#rows = query_job.result()  # Waits for query to finish
#for row in rows:
#    print(row.name)
print("se borro la tabla final")
query_job = bigquery_client.query(query3)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.name)
print("se populo la tabla final")

