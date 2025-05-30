from dataclasses import dataclass
from datetime import date


@dataclass
class Employee:
    employee_id: int
    name: str
    email: str
    department: str
    designation: str
    salary: float
    date_of_joining: date
