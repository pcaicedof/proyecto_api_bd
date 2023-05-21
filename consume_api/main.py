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

    
def main(event):
    consumer = ConsumeApi(
        event = event
    )
    consumer.read_csv_from_gcs()
    payload = consumer.get_payload()
    response = send_payload(payload, url)
    return response


event = {'bucket': 'prueba-globant', 'contentType': 'text/csv', 'crc32c': '0o8bEg==', 'etag': 'CN+DxtOHhf8CEAE=', 'generation': '1684625666703839', 'id': 'prueba-globant/files_to_migrate/jobs.csv/1684625666703839', 'kind': 'storage#object', 'md5Hash': 'qAxjXipEea9z5x/FWLjQFA==', 'mediaLink': 'https://storage.googleapis.com/download/storage/v1/b/prueba-globant/o/files_to_migrate%2Fjobs.csv?generation=1684625666703839&alt=media', 'metageneration': '1', 'name': 'files_to_migrate/jobs.csv', 'selfLink': 'https://www.googleapis.com/storage/v1/b/prueba-globant/o/files_to_migrate%2Fjobs.csv', 'size': '4419', 'storageClass': 'STANDARD', 'timeCreated': '2023-05-20T23:34:26.788Z', 'timeStorageClassUpdated': '2023-05-20T23:34:26.788Z', 'updated': '2023-05-20T23:34:26.788Z'}
response = main(event)
print(response)