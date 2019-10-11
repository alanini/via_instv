#!/usr/bin/python3
import numpy
#import google.cloud.bigquery
import os
import sys
from google.cloud import bigquery
query = """DROP TABLE datosTest.stage_IGTV8"""
dataset_id = 'datosTest'
#table_id = 'stage_IGTV8'
SERVICE_ACCOUNT_CREDENTIALS_FILE="/IGTV/warehouse.json"
PROJECT_ID="warehouse-245019"
bigquery_client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_CREDENTIALS_FILE, project=PROJECT_ID)


query_job = bigquery_client.query(query)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.name)
