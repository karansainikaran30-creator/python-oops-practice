import math
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

    @staticmethod
    def _validate_student_id(student_id):
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise ValueError("Student ID must be an integer.")

    @staticmethod
    def _validate_course(course):
        if not isinstance(course, str) or not course.strip():
            raise ValueError("Course cannot be empty.")

    @staticmethod
    def _validate_marks(marks):
        if (
            isinstance(marks, bool)
            or not isinstance(marks, (int, float))
            or not math.isfinite(marks)
            or not 0 <= marks <= 100
        ):
            raise ValueError("Invalid marks.")

    def _fetch_students(self, query, parameters=()):
        rows = self._get_connection().execute(query, parameters).fetchall()
        return [self._student_from_row(row) for row in rows]

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
        return self._fetch_students(
            "SELECT student_id, name, age, course, marks FROM students ORDER BY student_id"
        )

    def get_student_by_id(self, student_id):
        self._validate_student_id(student_id)
        students = self._fetch_students(
            "SELECT student_id, name, age, course, marks FROM students WHERE student_id = ?",
            (student_id,),
        )
        return students[0] if students else None

    def update_student(self, student_id, name=None, age=None, course=None, marks=None):
        self._validate_student_id(student_id)
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
        self._validate_student_id(student_id)
        connection = self._get_connection()
        try:
            cursor = connection.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            connection.commit()
            return cursor.rowcount == 1
        except sqlite3.Error:
            connection.rollback()
            raise

    def get_students_by_course(self, course):
        self._validate_course(course)
        return self._fetch_students(
            "SELECT student_id, name, age, course, marks FROM students WHERE course = ?",
            (course.strip(),),
        )

    def get_students_by_marks(self, min_marks):
        self._validate_marks(min_marks)
        return self._fetch_students(
            "SELECT student_id, name, age, course, marks FROM students WHERE marks >= ?",
            (min_marks,),
        )

    def search_students_by_name(self, keyword):
        if not isinstance(keyword, str) or not keyword.strip():
            raise ValueError("Search keyword cannot be empty.")
        pattern = f"%{keyword.strip()}%"
        return self._fetch_students(
            "SELECT student_id, name, age, course, marks FROM students WHERE name LIKE ?",
            (pattern,),
        )

    def get_students_sorted_by_marks(self, desc=True):
        order = "DESC" if desc else "ASC"
        return self._fetch_students(
            f"SELECT student_id, name, age, course, marks FROM students ORDER BY marks {order}"
        )

    def get_students_sorted_by_name(self):
        return self._fetch_students(
            "SELECT student_id, name, age, course, marks FROM students ORDER BY name ASC"
        )

    def get_top_students(self, limit):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise ValueError("Number of students must be greater than 0.")
        return self._fetch_students(
            "SELECT student_id, name, age, course, marks FROM students ORDER BY marks DESC LIMIT ?",
            (limit,),
        )

    def get_students_by_course_and_marks(self, course, min_marks):
        self._validate_course(course)
        self._validate_marks(min_marks)
        return self._fetch_students(
            "SELECT student_id, name, age, course, marks FROM students WHERE course = ? AND marks >= ?",
            (course.strip(), min_marks),
        )

    def get_students_by_either_course(self, first_course, second_course):
        self._validate_course(first_course)
        self._validate_course(second_course)
        return self._fetch_students(
            "SELECT student_id, name, age, course, marks FROM students WHERE course = ? OR course = ?",
            (first_course.strip(), second_course.strip()),
        )

    def get_total_students(self):
        row = self._get_connection().execute("SELECT COUNT(*) FROM students").fetchone()
        return row[0]

    def get_average_marks(self):
        row = self._get_connection().execute("SELECT AVG(marks) FROM students").fetchone()
        return row[0]

    def get_total_marks(self):
        row = self._get_connection().execute("SELECT COALESCE(SUM(marks), 0) FROM students").fetchone()
        return row[0]

    def get_highest_marks(self):
        row = self._get_connection().execute("SELECT MAX(marks) FROM students").fetchone()
        return row[0]

    def get_lowest_marks(self):
        row = self._get_connection().execute("SELECT MIN(marks) FROM students").fetchone()
        return row[0]

    def get_student_statistics(self):
        row = self._get_connection().execute(
            """
            SELECT COUNT(*) AS total_students,
                   COALESCE(SUM(marks), 0) AS total_marks,
                   AVG(marks) AS average_marks,
                   MAX(marks) AS highest_marks,
                   MIN(marks) AS lowest_marks
            FROM students
            """
        ).fetchone()
        return dict(row)

    def get_course_statistics(self):
        rows = self._get_connection().execute(
            """
            SELECT course,
                   COUNT(*) AS total_students,
                   AVG(marks) AS average_marks,
                   MAX(marks) AS highest_marks,
                   MIN(marks) AS lowest_marks
            FROM students
            GROUP BY course
            ORDER BY course ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def get_course_average_marks(self):
        rows = self._get_connection().execute(
            "SELECT course, AVG(marks) AS average_marks FROM students GROUP BY course ORDER BY course ASC"
        ).fetchall()
        return [dict(row) for row in rows]

    def get_course_highest_marks(self):
        rows = self._get_connection().execute(
            "SELECT course, MAX(marks) AS highest_marks FROM students GROUP BY course ORDER BY course ASC"
        ).fetchall()
        return [dict(row) for row in rows]

    def get_course_lowest_marks(self):
        rows = self._get_connection().execute(
            "SELECT course, MIN(marks) AS lowest_marks FROM students GROUP BY course ORDER BY course ASC"
        ).fetchall()
        return [dict(row) for row in rows]

    def get_courses_above_average(self, min_average):
        if (
            isinstance(min_average, bool)
            or not isinstance(min_average, (int, float))
            or not math.isfinite(min_average)
            or not 0 <= min_average <= 100
        ):
            raise ValueError("Minimum average must be between 0 and 100.")
        rows = self._get_connection().execute(
            """
            SELECT course, AVG(marks) AS average_marks
            FROM students
            GROUP BY course
            HAVING AVG(marks) >= ?
            ORDER BY course ASC
            """,
            (min_average,),
        ).fetchall()
        return [dict(row) for row in rows]

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None