import math
import sqlite3
from pathlib import Path

from course import Course
from student import Student


class Database:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else Path(__file__).with_name("student_management.db")
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection

    def _get_connection(self):
        if self.connection is None:
            raise RuntimeError("Connect to the database before using it.")
        return self.connection

    def create_course_table(self):
        self._get_connection().execute(
            """
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL UNIQUE CHECK (length(trim(course_name)) > 0)
            )
            """
        )
        self._get_connection().commit()

    def create_table(self):
        self._get_connection().execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL CHECK (length(trim(name)) > 0),
                age INTEGER NOT NULL CHECK (age > 0),
                course_id INTEGER NOT NULL,
                marks REAL NOT NULL CHECK (marks BETWEEN 0 AND 100),
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
            """
        )
        self._get_connection().commit()

    @staticmethod
    def _validate_student_id(student_id):
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise ValueError("Student ID must be an integer.")

    @staticmethod
    def _validate_course_id(course_id):
        if isinstance(course_id, bool) or not isinstance(course_id, int):
            raise ValueError("Course ID must be an integer.")

    @staticmethod
    def _validate_marks(marks):
        if (
            isinstance(marks, bool)
            or not isinstance(marks, (int, float))
            or not math.isfinite(marks)
            or not 0 <= marks <= 100
        ):
            raise ValueError("Invalid marks.")

    @staticmethod
    def _student_from_row(row):
        return Student(row["student_id"], row["name"], row["age"], row["course_id"], row["marks"])

    def add_course(self, course):
        course.validate()
        connection = self._get_connection()
        try:
            cursor = connection.execute(
                "INSERT INTO courses (course_id, course_name) VALUES (?, ?)",
                (course.course_id, course.course_name.strip()),
            )
            connection.commit()
            return cursor.rowcount == 1
        except sqlite3.Error:
            connection.rollback()
            raise

    def get_all_courses(self):
        rows = self._get_connection().execute(
            "SELECT course_id, course_name FROM courses ORDER BY course_id"
        ).fetchall()
        return [Course(row["course_id"], row["course_name"]) for row in rows]

    def get_course_by_id(self, course_id):
        self._validate_course_id(course_id)
        row = self._get_connection().execute(
            "SELECT course_id, course_name FROM courses WHERE course_id = ?",
            (course_id,),
        ).fetchone()
        return Course(row["course_id"], row["course_name"]) if row else None

    def delete_course(self, course_id):
        self._validate_course_id(course_id)
        connection = self._get_connection()
        try:
            cursor = connection.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
            connection.commit()
            return cursor.rowcount == 1
        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise ValueError("Cannot delete a course that has students.") from error
        except sqlite3.Error:
            connection.rollback()
            raise

    def add_student(self, student):
        student.validate()
        connection = self._get_connection()
        if self.get_course_by_id(student.course_id) is None:
            raise ValueError("Invalid course ID.")
        try:
            cursor = connection.execute(
                """
                INSERT INTO students (student_id, name, age, course_id, marks)
                VALUES (?, ?, ?, ?, ?)
                """,
                (student.student_id, student.name.strip(), student.age, student.course_id, student.marks),
            )
            connection.commit()
            return cursor.rowcount == 1
        except sqlite3.Error:
            connection.rollback()
            raise

    def get_all_students(self):
        rows = self._get_connection().execute(
            "SELECT student_id, name, age, course_id, marks FROM students ORDER BY student_id"
        ).fetchall()
        return [self._student_from_row(row) for row in rows]

    def get_student_by_id(self, student_id):
        self._validate_student_id(student_id)
        row = self._get_connection().execute(
            "SELECT student_id, name, age, course_id, marks FROM students WHERE student_id = ?",
            (student_id,),
        ).fetchone()
        return self._student_from_row(row) if row else None

    def update_student(self, student_id, name=None, age=None, course_id=None, marks=None):
        self._validate_student_id(student_id)
        current = self.get_student_by_id(student_id)
        if current is None:
            return False

        updated = Student(
            student_id,
            current.name if name is None else name,
            current.age if age is None else age,
            current.course_id if course_id is None else course_id,
            current.marks if marks is None else marks,
        )
        updated.validate()
        if self.get_course_by_id(updated.course_id) is None:
            raise ValueError("Invalid course ID.")

        assignments = []
        values = []
        for column, value in (("name", name), ("age", age), ("course_id", course_id), ("marks", marks)):
            if value is not None:
                assignments.append(f"{column} = ?")
                values.append(value.strip() if column == "name" else value)
        if not assignments:
            raise ValueError("Provide at least one field to update.")

        values.append(student_id)
        connection = self._get_connection()
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

    def get_students_with_courses(self):
        rows = self._get_connection().execute(
            """
            SELECT s.student_id, s.name, s.age, c.course_id, c.course_name, s.marks
            FROM students AS s
            INNER JOIN courses AS c ON s.course_id = c.course_id
            ORDER BY s.student_id
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def get_student_with_course_by_id(self, student_id):
        self._validate_student_id(student_id)
        row = self._get_connection().execute(
            """
            SELECT s.student_id, s.name, s.age, c.course_id, c.course_name, s.marks
            FROM students AS s
            INNER JOIN courses AS c ON s.course_id = c.course_id
            WHERE s.student_id = ?
            """,
            (student_id,),
        ).fetchone()
        return dict(row) if row else None

    def get_students_by_course(self, course_name):
        if not isinstance(course_name, str) or not course_name.strip():
            raise ValueError("Course name cannot be empty.")
        rows = self._get_connection().execute(
            """
            SELECT s.student_id, s.name, s.age, c.course_id, c.course_name, s.marks
            FROM students AS s
            INNER JOIN courses AS c ON s.course_id = c.course_id
            WHERE c.course_name = ?
            ORDER BY s.student_id
            """,
            (course_name.strip(),),
        ).fetchall()
        return [dict(row) for row in rows]

    def get_students_by_marks(self, min_marks):
        self._validate_marks(min_marks)
        rows = self._get_connection().execute(
            """
            SELECT s.student_id, s.name, s.age, c.course_id, c.course_name, s.marks
            FROM students AS s
            INNER JOIN courses AS c ON s.course_id = c.course_id
            WHERE s.marks >= ?
            ORDER BY s.student_id
            """,
            (min_marks,),
        ).fetchall()
        return [dict(row) for row in rows]

    def get_students_sorted(self, sort_by="marks", desc=True):
        columns = {"marks": "s.marks", "name": "s.name"}
        if sort_by not in columns:
            raise ValueError("Sort by marks or name only.")
        direction = "DESC" if desc else "ASC"
        rows = self._get_connection().execute(
            f"""
            SELECT s.student_id, s.name, s.age, c.course_id, c.course_name, s.marks
            FROM students AS s
            INNER JOIN courses AS c ON s.course_id = c.course_id
            ORDER BY {columns[sort_by]} {direction}
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def get_top_students(self, limit):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise ValueError("Number of students must be greater than 0.")
        rows = self._get_connection().execute(
            """
            SELECT s.student_id, s.name, s.age, c.course_id, c.course_name, s.marks
            FROM students AS s
            INNER JOIN courses AS c ON s.course_id = c.course_id
            ORDER BY s.marks DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]

    def search_students_by_name(self, keyword):
        if not isinstance(keyword, str) or not keyword.strip():
            raise ValueError("Search keyword cannot be empty.")
        rows = self._get_connection().execute(
            """
            SELECT s.student_id, s.name, s.age, c.course_id, c.course_name, s.marks
            FROM students AS s
            INNER JOIN courses AS c ON s.course_id = c.course_id
            WHERE s.name LIKE ?
            ORDER BY s.student_id
            """,
            (f"%{keyword.strip()}%",),
        ).fetchall()
        return [dict(row) for row in rows]

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
            SELECT c.course_id, c.course_name,
                   COUNT(s.student_id) AS total_students,
                   AVG(s.marks) AS average_marks,
                   MAX(s.marks) AS highest_marks,
                   MIN(s.marks) AS lowest_marks
            FROM courses AS c
            LEFT JOIN students AS s ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
            ORDER BY c.course_id
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def get_courses_without_students(self):
        rows = self._get_connection().execute(
            """
            SELECT c.course_id, c.course_name
            FROM courses AS c
            LEFT JOIN students AS s ON c.course_id = s.course_id
            WHERE s.student_id IS NULL
            ORDER BY c.course_id
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def get_courses_above_average(self, min_average):
        self._validate_marks(min_average)
        rows = self._get_connection().execute(
            """
            SELECT c.course_id, c.course_name, AVG(s.marks) AS average_marks
            FROM courses AS c
            INNER JOIN students AS s ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
            HAVING AVG(s.marks) >= ?
            ORDER BY c.course_id
            """,
            (min_average,),
        ).fetchall()
        return [dict(row) for row in rows]

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None