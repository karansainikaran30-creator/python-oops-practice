import sqlite3

from student import Student


class DuplicateStudentError(Exception):
    """Raised when an existing student ID is inserted again."""


class Database:
    def __init__(self, database_path="student_management.db"):
        self.database_path = database_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.database_path)
        return self.connection

    def create_table(self):
        connection = self._get_connection()
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK (age > 0),
                course TEXT NOT NULL,
                marks REAL NOT NULL CHECK (marks >= 0 AND marks <= 100)
            )
            """
        )
        connection.commit()

    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("student must be a validated Student object.")

        connection = self._get_connection()
        try:
            connection.execute(
                """
                INSERT INTO students (student_id, name, age, course, marks)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    student.student_id,
                    student.name,
                    student.age,
                    student.course,
                    student.marks,
                ),
            )
            connection.commit()
        except sqlite3.IntegrityError as error:
            connection.rollback()
            error_name = getattr(error, "sqlite_errorname", "")
            error_message = str(error).lower()
            if error_name == "SQLITE_CONSTRAINT_PRIMARYKEY" or (
                "student_id" in error_message
                and ("unique" in error_message or "primary key" in error_message)
            ):
                raise DuplicateStudentError("Student ID already exists.") from error
            raise
        except sqlite3.Error:
            connection.rollback()
            raise

    def get_all_students(self):
        cursor = self._get_connection().execute(
            """
            SELECT student_id, name, age, course, marks
            FROM students
            ORDER BY student_id
            """
        )
        return cursor.fetchall()

    def get_student_by_id(self, student_id):
        cursor = self._get_connection().execute(
            """
            SELECT student_id, name, age, course, marks
            FROM students
            WHERE student_id = ?
            """,
            (student_id,),
        )
        return cursor.fetchone()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def _get_connection(self):
        if self.connection is None:
            raise sqlite3.ProgrammingError("Connect to the database before using it.")
        return self.connection