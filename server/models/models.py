from pydantic import BaseModel, EmailStr
from dataclasses import dataclass
from datetime import date


@dataclass
class Employee:
    employee_id: int
    name: str
    email: str
    department: str
    designation: str
    salary: int
    date_of_joining: date


class EmployeeIn(BaseModel):
    employee_id: int
    name: str
    email: EmailStr
    department: str
    designation: str
    salary: int
    date_of_joining: date
