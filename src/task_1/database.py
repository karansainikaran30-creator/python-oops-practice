import sqlite3


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
                student_id INTEGER,
                name TEXT,
                age INTEGER,
                course TEXT,
                marks REAL
            )
            """
        )
        connection.commit()

    def add_student(self, student):
        connection = self._get_connection()
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

    def get_all_students(self):
        cursor = self._get_connection().execute(
            "SELECT student_id, name, age, course, marks FROM students ORDER BY student_id"
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