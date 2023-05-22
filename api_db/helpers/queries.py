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

DELETE_TABLE_QUERY = """
    delete from {table}
"""

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
    where extract(YEAR from date) = {year})
    PIVOT(COUNT(employee_id) FOR quarter IN ('Q1',
      'Q2',
      'Q3',
      'Q4'))
      order by department, job
"""

EMPLOYEES_BY_DEPT = """
  with departments as (SELECT
    d.id,
    d.department,
    DATE(PARSE_DATETIME('%Y-%m-%dT%H:%M:%S',REPLACE(he.datetime,'Z',''))) date,
    he.id employee_id
  FROM
    `{project}`.{dataset}.hired_employees he
  JOIN
    `{project}`.{dataset}.departments d
  ON

    he.department_id = d.id ),

employees_avg as (
select avg(employees_number) employees_number_avg
from (
  select department, count(employee_id) employees_number
  from departments
  where extract(YEAR from date) = {year}
  group by department
)
)

 select id, department, count(employee_id) employees_number
  from departments
  group by id, department
  having count(employee_id) > (select employees_number_avg from employees_avg)
  order by employees_number desc
"""