#Python
from typing import Optional
import json
#pydantic
from pydantic import ValidationError
#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form, File, UploadFile
from fastapi import status
from fastapi import HTTPException

from api_db.helpers.schemas import Payload, RestorePayload
from api_db.helpers.constants import SCHEMA_QUERY, TABLE_QUERY, AVRO_SCHEMA, DELETE_TABLE_QUERY
from api_db.helpers.utils import (
    get_dataframe_from_json,
    connect_to_db,
    get_tables_from_db,
    get_avro_file_from_df,
    get_df_from_avro,
    execute_query)

app = FastAPI()


@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    result = {"hello": "world"}
    return result


@app.post(
    path="/migration",
    status_code=status.HTTP_200_OK
)
def migrate_tables(payload: Payload = Body(...)):
    dict_payload =payload.dict()
    df_table = get_dataframe_from_json(dict_payload)
    connection = connect_to_db()
    table_name = dict_payload['table'].value
    df_table.to_sql(table_name, connection, if_exists='replace', index=False)
    connection.close()
    return payload

@app.post(
    path="/createBackup",
    status_code=status.HTTP_200_OK
)
def get_backup_from_db():
    df_table_list = get_tables_from_db(SCHEMA_QUERY)
    for index, row in df_table_list.iterrows():
        table = row['name']
        final_query_table = TABLE_QUERY.format(table=table)
        print(final_query_table)
        df_table = get_tables_from_db(final_query_table)
        get_avro_file_from_df(df_table, table, AVRO_SCHEMA[table])
        print(df_table)
    return print("ok")

@app.post(
    path="/restoreBackup",
    status_code=status.HTTP_200_OK
)
def restore_backup_from_avro(restore_payload: RestorePayload = Body(...)):
    dict_restore = restore_payload.dict()
    restore_table = dict_restore['table'].value
    backup_date = dict_restore['backup_date']
    print(backup_date)
    execute_query(DELETE_TABLE_QUERY.format(table=restore_table))
    connection = connect_to_db()
    file = f'./backup/{backup_date}/{restore_table}.avro'
    df_table = get_df_from_avro(file)
    df_table.to_sql(restore_table, connection, if_exists='replace', index=False)
    return print("ok")
