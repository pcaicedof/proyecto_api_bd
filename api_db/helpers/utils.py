from pydantic import ValidationError
from api_db.helpers.schemas import Job, Deparment, HiredEmployee
from api_db.helpers.constants import (
    DB_PATH, BUCKET_NAME, GCP_PROJECT_ID, GCP_DATASET)
import pandas as pd
import sqlite3
import fastavro
import os
from datetime import datetime
from google.cloud import storage
from google.cloud import bigquery as bq
import os


def validate_row(row, model):
    try:
        model_instance = model(**row)
    except ValidationError as e:
        print("Error de validación:")
        print(e)

def get_dataframe_from_json(dict_payload):
    json_data = dict_payload['data']
    row_list = []
    for index_row, data in enumerate(json_data):
        row = json_data[index_row]
        if dict_payload['table'].value == 'jobs':
            validate_row(row, Job)
        elif dict_payload['table'].value == 'departments':
            validate_row(row, Deparment)
        elif dict_payload['table'].value == 'hired_employees':
            validate_row(row, HiredEmployee)
        if index_row == 1000:
            break
        row_list.append(row)
    df_table = pd.DataFrame(row_list)
    return df_table


def connect_to_db():
    connection = sqlite3.connect(DB_PATH)
    return connection

def execute_query(query):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.close()
    return cursor


def get_tables_from_db(query):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    connection.close()
    df = pd.DataFrame(rows, columns=columns)
    return df


def write_avro_to_gcs(df, table_name, avro_schema):
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    data = df.to_dict('records')
    schema = {
    'type': 'record',
    'name': 'YourSchemaName',
    'fields': avro_schema
        }
    temp_file = f'/tmp/{table_name}.avro'
    with open(temp_file, "wb") as avro_file:
        fastavro.writer(avro_file, schema, data)
    date_folder = datetime.now().date()
    file_name = f'backup/{date_folder}/{table_name}.avro'
    blob = bucket.blob(file_name)
    blob.upload_from_filename(temp_file)
    os.remove(temp_file)

def create_temp_file(folder_name, file):
    temp_dir = folder_name
    os.makedirs(temp_dir, exist_ok=True)
    temp_file = os.path.join(temp_dir, file)
    return temp_file

def get_df_from_avro(backup_date, file):
    folder = f'backup/{backup_date}'
    temp_file = create_temp_file(folder, file)
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(temp_file)
    blob.download_to_filename(temp_file)
    avro_file = open(temp_file, 'rb')
    avro_reader = fastavro.reader(avro_file)
    records = []
    for record in avro_reader:
        records.append(record)
    df = pd.DataFrame(records)
    avro_file.close()
    os.remove(temp_file)
    return df

def write_to_bq_from_df(project, dataset, table_name, df):
    bq_client = bq.Client(project=project)
    dataset_ref = bq_client.dataset(dataset)
    table_ref = dataset_ref.table(table_name)
    job_config = bq.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

    try:
        bq_client.load_table_from_dataframe(df,
                                            table_ref,
                                            job_config=job_config
                                            ).result()
    except Exception as e:
        print(e)
