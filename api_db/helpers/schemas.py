#Python
from enum import Enum
from datetime import datetime
#Pydantic
from pydantic import BaseModel, validator
from pydantic import Field
from typing import List


class Tables(Enum):
    hired_employees = "hired_employees"
    jobs = "jobs"
    departments = "departments"

class Payload(BaseModel):
    table: Tables = Field(...)
    data: List[dict]

class Job(BaseModel):
    id: int
    job: str

    @validator('id')
    def validate_field1(cls, value):
        # Realiza validaciones o transformaciones en el valor de field1
        if not isinstance(value, int):
            raise ValueError("El campo field2 debe ser un número entero")
        return value

class Deparment(BaseModel):
    id: int
    department: str

class HiredEmployee(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int