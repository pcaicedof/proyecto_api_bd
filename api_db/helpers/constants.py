DB_PATH = '/app/api_db/db/company.db'

AVRO_SCHEMA = {
    'jobs': [
        {'name': 'id', 'type': 'int'},
        {'name': 'job', 'type': 'string'}
    ],
    'departments' : [
        {'name': 'id', 'type': 'int'},
        {'name': 'department', 'type': 'string'}
    ],
    'hired_employees': [
        {'name': 'id', 'type': 'int'},
        {'name': 'name', 'type': 'string'},
        {'name': 'datetime', 'type': 'string'},
        {'name': 'department_id', 'type': 'int'},
        {'name': 'job_id', 'type': 'int'},
    ]
}

GCP_PROJECT_ID = "prueba-globant"

GCP_DATASET = "company"

GCP_REPORT_DATASET = 'reports'

BUCKET_NAME = 'prueba-globant'
