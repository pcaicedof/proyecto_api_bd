#FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import status
from fastapi import HTTPException

from api_db.helpers.schemas import Payload, RestorePayload
from api_db.helpers.constants import (
    SCHEMA_QUERY, TABLE_QUERY, AVRO_SCHEMA, DELETE_TABLE_QUERY,
    GCP_PROJECT_ID, GCP_DATASET)
from api_db.helpers.utils import (
    get_dataframe_from_json,
    connect_to_db,
    get_tables_from_db,
    get_df_from_avro,
    execute_query,
    write_avro_to_gcs,
    write_to_bq_from_df)


app = FastAPI()


@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    result = {"Proyecto": "Desarrollo de API"}
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
    try:
        df_table.to_sql(table_name, connection, if_exists='replace', index=False)
        status = 'ok'
    except Exception as e:
        status = 'failed'
    connection.close()
    response = {table_name: status}
    return response

@app.post(
    path="/createBackup",
    status_code=status.HTTP_200_OK
)
def get_backup_from_db():
    df_table_list = get_tables_from_db(SCHEMA_QUERY)
    response = {}
    for index, row in df_table_list.iterrows():
        table = row['name']
        final_query_table = TABLE_QUERY.format(table=table)
        df_table = get_tables_from_db(final_query_table)
        write_to_bq_from_df(GCP_PROJECT_ID, GCP_DATASET, table, df_table)
        try:
            write_avro_to_gcs(df_table, table, AVRO_SCHEMA[table])
            status = 'ok'
        except Exception as e:
            status = 'failed'
        response[table] = status
    return response

@app.post(
    path="/restoreBackup",
    status_code=status.HTTP_200_OK
)
def restore_backup_from_avro(restore_payload: RestorePayload = Body(...)):
    dict_restore = restore_payload.dict()
    restore_table = dict_restore['table'].value
    backup_date = dict_restore['backup_date']
    execute_query(DELETE_TABLE_QUERY.format(table=restore_table))
    connection = connect_to_db()
    file = f'{restore_table}.avro'
    df_table = get_df_from_avro(backup_date, file)
    try:
        df_table.to_sql(restore_table, connection, if_exists='replace', index=False)
        status = 'ok'
    except Exception as e:
        status = 'failed'
    response = {restore_table: status}
    return response
