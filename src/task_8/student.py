"""Student model used by the command-line application."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Student:
    student_id: int
    name: str
    age: int
    course_id: int
    marks: Decimal
    course_name: str = ""
