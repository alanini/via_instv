#!/usr/bin/python3
from google.cloud import bigquery
import os
import shutil
#client = bigquery.Client()
#filename = 'C:\\Rocking Data\\Clientes\\Viacom\\WebScraping\\archivos\\comedycentralla2019-08-18.csv'
#filename = 'C:\\Rocking Data\\Clientes\\Viacom\\WebScraping\\subida16082019.csv'
dataset_id = 'datosTest'
table_id = 'stage_IGTV8'
SERVICE_ACCOUNT_CREDENTIALS_FILE="/IGTV/warehouse.json"
PROJECT_ID="warehouse-245019"
bigquery_client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_CREDENTIALS_FILE, project=PROJECT_ID)
dataset_ref = bigquery_client.dataset(dataset_id)
table_ref = dataset_ref.table(table_id)
job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1
#job_config.
job_config.autodetect = True


files = [i for i in os.listdir("/IGTV/archivos") if i.endswith("csv")]
#files = ['C:\\Rocking Data\\Clientes\\Viacom\\WebScraping\\subida16082019.csv']
for archivo in files:
    print(archivo)
    filename="/IGTV/archivos/"+archivo
    #filename='C:\\Rocking Data\\Clientes\\Viacom\\WebScraping\\subida16082019.csv'
    with open(filename, "rb") as source_file:
        job = bigquery_client.load_table_from_file(
        source_file,
        table_ref,
        location="US",  # Must match the destination dataset location.
        job_config=job_config,
        )  # API request

        try:
            job.result()  # Waits for table load to complete.
        except:
            print(job.errors)
        print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))
    shutil.move(filename,"/IGTV/historico/"+archivo)
    print("movio", filename)


