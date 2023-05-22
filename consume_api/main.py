import pandas as pd
import json
from utils.constants import columns, url
from utils.helpers import send_payload
from google.cloud import storage

def read_csv_from_gcs(bucket_name, file_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    csv_data = blob.download_as_text()
    df = pd.read_csv(pd.compat.StringIO(csv_data))
    return df

class ConsumeApi():

    def __init__(self, event):
        self.event = event

    def read_csv_from_gcs(self):
        split_path = self.event['name'].split('/')
        table = split_path[-1].replace('.csv','')
        schema = columns[table]
        colnames = list(schema.keys())
        bucket_name = self.event['bucket']
        file_name = self.event['name']
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        file = f'gcs://{bucket_name}/{file_name}'
        df = pd.read_csv(file,
                         delimiter=",",
                         dtype = schema,
                         names=colnames,
                         na_values='')
        df = df.dropna()
        return table, df

    def get_payload(self):
        payload = {}
        table, df = self.read_csv_from_gcs()
        data = df.to_dict('records')
        payload['table'] = table
        payload['data'] = data
        return payload

    
def main(event, context):
    consumer = ConsumeApi(
        event = event
    )
    consumer.read_csv_from_gcs()
    payload = consumer.get_payload()
    response = send_payload(payload, url)
    return response