import pandas as pd
import json
from utils.constants import columns, url
from utils.helpers import send_payload



class ConsumeApi():

    def __init__(self, path):
        self.path = path


    def get_df_from_csv(self):
        split_path = self.path.split('/')
        table = split_path[-1].replace('.csv','')
        schema = columns[table]
        colnames = list(schema.keys())
        df = pd.read_csv(
            self.path,
            delimiter=",",
            dtype = schema,
            names=colnames,
            na_values=''
            )
        df = df.dropna()
        return table, df

    def get_payload(self):
        payload = {}
        table, df = self.get_df_from_csv()
        data = df.to_dict('records')
        payload['table'] = table
        payload['data'] = data
        return payload

    
def main(path):
    consumer = ConsumeApi(
        path = path
    )
    consumer.get_df_from_csv()
    payload = consumer.get_payload()
    response = send_payload(payload, url)
    return response

response = main('./files/hired_employees.csv')
print(response)