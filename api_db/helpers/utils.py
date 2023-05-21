import json
from pydantic import ValidationError
from api_db.helpers.schemas import Job, Deparment, HiredEmployee
from api_db.helpers.constants import DB_PATH
import pandas as pd
import sqlite3
import fastavro
import os
from datetime import datetime

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
        else:
            print('no entra')
        if index_row == 1000:
            break
        row_list.append(row)
    df_table = pd.DataFrame(row_list)
    return df_table


def connect_to_db():
    print(DB_PATH)
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

def get_folders():
    rootdir = './backup'
    folder_list = os.listdir(rootdir)
    for idx, file in enumerate(folder_list):
        folder_path = os.path.join(rootdir, file)
        if os.path.isdir(folder_path):
            folder_name = folder_path.replace(rootdir+'/', '')
            folder_number = idx + 1
            print(f'{folder_number}. {folder_name}')
    return folder_list

def create_folder(name):
    path = f'./backup/{name}'
    os.makedirs(path)
    return path

def get_avro_file_from_df(df,table_name, avro_schema):
    data = df.to_dict('records')
    schema = {
    'type': 'record',
    'name': 'YourSchemaName',
    'fields': avro_schema
        }
    folder_list = get_folders()
    date_folder = datetime.now().date()
    if date_folder in folder_list:
        path = create_folder(date_folder)
    path = f'./backup/{date_folder}'
    with open(f'{path}/{table_name}.avro', 'wb') as avro_file:
        fastavro.writer(avro_file, schema, data)

def get_df_from_avro(file):
    avro_file = open(file, 'rb')
    avro_reader = fastavro.reader(avro_file)
    records = []
    for record in avro_reader:
        records.append(record)
    df = pd.DataFrame(records)
    avro_file.close()
    return df