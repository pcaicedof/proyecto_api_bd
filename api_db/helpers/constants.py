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
GCP_PROJECT_ID = "prueba-globant"

GCP_DATASET = "company"

GCP_REPORT_DATASET = 'reports'

BUCKET_NAME = 'prueba-globant'

EMPLOYEES_BY_QUARTER = """
WITH
  employees AS (
  SELECT
    d.department,
    j.job,
    DATE(PARSE_DATETIME('%Y-%m-%dT%H:%M:%S',REPLACE(he.datetime,'Z',''))) date,
    EXTRACT(QUARTER
    FROM
      DATE(PARSE_DATETIME('%Y-%m-%dT%H:%M:%S',REPLACE(he.datetime,'Z','')))) quarter,
    he.id employee_id
  FROM
    `{project}`.{dataset}.hired_employees he
  JOIN
    `{project}`.{dataset}.jobs j
  ON
    he.job_id = j.id
  JOIN
    `{project}`.{dataset}.departments d
  ON

    he.department_id = d.id)

SELECT
  *
FROM (
  SELECT
    department,
    job,
    employee_id,
    CONCAT('Q',quarter) quarter
  FROM
    employees
    where extract(YEAR from date) = {{year}})
    PIVOT(COUNT(employee_id) FOR quarter IN ('Q1',
      'Q2',
      'Q3',
      'Q4'))
      order by department, job
""".format(project=GCP_PROJECT_ID, dataset=GCP_DATASET)