import sqlite3
from pathlib import Path

from student import Student


class Database:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else Path(__file__).with_name("student_management.db")
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def _get_connection(self):
        if self.connection is None:
            raise RuntimeError("Connect to the database before using it.")
        return self.connection

    def create_table(self):
        connection = self._get_connection()
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL CHECK (length(trim(name)) > 0),
                age INTEGER NOT NULL CHECK (age > 0),
                course TEXT NOT NULL CHECK (length(trim(course)) > 0),
                marks REAL NOT NULL CHECK (marks BETWEEN 0 AND 100)
            )
            """
        )
        connection.commit()

    @staticmethod
    def _student_from_row(row):
        return Student(row["student_id"], row["name"], row["age"], row["course"], row["marks"])

    def add_student(self, student):
        student.validate()
        connection = self._get_connection()
        try:
            cursor = connection.execute(
                """
                INSERT INTO students (student_id, name, age, course, marks)
                VALUES (?, ?, ?, ?, ?)
                """,
                (student.student_id, student.name.strip(), student.age, student.course.strip(), student.marks),
            )
            connection.commit()
            return cursor.rowcount == 1
        except sqlite3.Error:
            connection.rollback()
            raise

    def get_all_students(self):
        connection = self._get_connection()
        rows = connection.execute(
            "SELECT student_id, name, age, course, marks FROM students ORDER BY student_id"
        ).fetchall()
        return [self._student_from_row(row) for row in rows]

    def get_student_by_id(self, student_id):
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise ValueError("Student ID must be an integer.")
        connection = self._get_connection()
        row = connection.execute(
            "SELECT student_id, name, age, course, marks FROM students WHERE student_id = ?",
            (student_id,),
        ).fetchone()
        return self._student_from_row(row) if row else None

    def update_student(self, student_id, name=None, age=None, course=None, marks=None):
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise ValueError("Student ID must be an integer.")

        connection = self._get_connection()
        current = self.get_student_by_id(student_id)
        if current is None:
            return False

        updated = Student(
            student_id,
            current.name if name is None else name,
            current.age if age is None else age,
            current.course if course is None else course,
            current.marks if marks is None else marks,
        )
        updated.validate()

        assignments = []
        values = []
        for column, value in (("name", name), ("age", age), ("course", course), ("marks", marks)):
            if value is not None:
                assignments.append(f"{column} = ?")
                values.append(value.strip() if column in ("name", "course") else value)
        if not assignments:
            raise ValueError("Provide at least one field to update.")

        values.append(student_id)
        try:
            cursor = connection.execute(
                f"UPDATE students SET {', '.join(assignments)} WHERE student_id = ?",
                values,
            )
            connection.commit()
            return cursor.rowcount == 1
        except sqlite3.Error:
            connection.rollback()
            raise

    def delete_student(self, student_id):
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise ValueError("Student ID must be an integer.")
        connection = self._get_connection()
        try:
            cursor = connection.execute(
                "DELETE FROM students WHERE student_id = ?",
                (student_id,),
            )
            connection.commit()
            return cursor.rowcount == 1
        except sqlite3.Error:
            connection.rollback()
            raise

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None