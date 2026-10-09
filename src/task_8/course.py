"""Course model used by the command-line application."""

from dataclasses import dataclass


@dataclass
class Course:
    course_id: int
    course_name: str
