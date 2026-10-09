"""Student model used by the command-line application."""

from dataclasses import dataclass


@dataclass
class Student:
    student_id: int
    name: str
    age: int
    email: str
    marks: float
    course_id: int
    course_name: str = ""
