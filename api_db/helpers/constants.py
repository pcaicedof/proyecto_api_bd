DB_PATH = '/app/api_db/db/company.db'

SCHEMA_QUERY = """
    SELECT 
        name
    FROM 
        sqlite_schema
    WHERE type = 'table'
"""

TABLE_QUERY = """
select *
from {table}
"""

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

DELETE_TABLE_QUERY = """
    delete from {table}
"""