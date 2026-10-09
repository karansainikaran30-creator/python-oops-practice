"""SQLite persistence and transaction handling for the student management system."""

import sqlite3
from pathlib import Path
from typing import Any


class Database:
    def __init__(self, db_path: str | Path = "student_management.db") -> None:
        self.db_path = str(db_path)
        self.connection = sqlite3.connect(self.db_path, isolation_level=None)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    def create_tables(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK (age > 0),
                email TEXT NOT NULL UNIQUE,
                marks REAL NOT NULL CHECK (marks >= 0 AND marks <= 100),
                course_id INTEGER NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            );
            """
        )
        self.create_history_table()

    def create_history_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS student_course_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                old_course_id INTEGER NOT NULL,
                new_course_id INTEGER NOT NULL,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (old_course_id) REFERENCES courses(course_id),
                FOREIGN KEY (new_course_id) REFERENCES courses(course_id)
            )
            """
        )

    def add_course(self, course_name: str) -> int:
        cursor = self.connection.execute(
            "INSERT INTO courses (course_name) VALUES (?)", (course_name.strip(),)
        )
        return int(cursor.lastrowid)

    def get_courses(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT course_id, course_name FROM courses ORDER BY course_id"
        ).fetchall()
        return [dict(row) for row in rows]

    def add_student(
        self, name: str, age: int, email: str, marks: float, course_id: int
    ) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO students (name, age, email, marks, course_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name.strip(), age, email.strip(), marks, course_id),
        )
        return int(cursor.lastrowid)

    def get_all_students(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT s.student_id, s.name, s.age, s.email, s.marks,
                   s.course_id, c.course_name
            FROM students AS s
            JOIN courses AS c ON c.course_id = s.course_id
            ORDER BY s.student_id
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def search_student(self, student_id: int) -> dict[str, Any] | None:
        row = self.connection.execute(
            """
            SELECT s.student_id, s.name, s.age, s.email, s.marks,
                   s.course_id, c.course_name
            FROM students AS s
            JOIN courses AS c ON c.course_id = s.course_id
            WHERE s.student_id = ?
            """,
            (student_id,),
        ).fetchone()
        return dict(row) if row is not None else None

    def search_students_by_course(self, course_id: int) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT s.student_id, s.name, s.age, s.email, s.marks,
                   s.course_id, c.course_name
            FROM students AS s
            JOIN courses AS c ON c.course_id = s.course_id
            WHERE s.course_id = ?
            ORDER BY s.name
            """,
            (course_id,),
        ).fetchall()
        return [dict(row) for row in rows]

    def search_students_by_marks(
        self, minimum: float, maximum: float
    ) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT s.student_id, s.name, s.age, s.email, s.marks,
                   s.course_id, c.course_name
            FROM students AS s
            JOIN courses AS c ON c.course_id = s.course_id
            WHERE s.marks BETWEEN ? AND ?
            ORDER BY s.marks DESC, s.student_id
            """,
            (minimum, maximum),
        ).fetchall()
        return [dict(row) for row in rows]

    def sort_students(
        self, order_by: str = "marks", descending: bool = False
    ) -> list[dict[str, Any]]:
        columns = {
            "student_id": "s.student_id",
            "name": "s.name",
            "age": "s.age",
            "marks": "s.marks",
            "course": "c.course_name",
        }
        if order_by not in columns:
            raise ValueError(f"Unsupported sort field: {order_by}")
        direction = "DESC" if descending else "ASC"
        rows = self.connection.execute(
            f"""
            SELECT s.student_id, s.name, s.age, s.email, s.marks,
                   s.course_id, c.course_name
            FROM students AS s
            JOIN courses AS c ON c.course_id = s.course_id
            ORDER BY {columns[order_by]} {direction}, s.student_id
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def top_n_students(self, count: int) -> list[dict[str, Any]]:
        if count <= 0:
            raise ValueError("The number of students must be positive.")
        rows = self.connection.execute(
            """
            SELECT s.student_id, s.name, s.age, s.email, s.marks,
                   s.course_id, c.course_name
            FROM students AS s
            JOIN courses AS c ON c.course_id = s.course_id
            ORDER BY s.marks DESC, s.student_id
            LIMIT ?
            """,
            (count,),
        ).fetchall()
        return [dict(row) for row in rows]

    def update_student(
        self,
        student_id: int,
        name: str,
        age: int,
        email: str,
        marks: float,
        course_id: int,
    ) -> bool:
        cursor = self.connection.execute(
            """
            UPDATE students
            SET name = ?, age = ?, email = ?, marks = ?, course_id = ?
            WHERE student_id = ?
            """,
            (name.strip(), age, email.strip(), marks, course_id, student_id),
        )
        return cursor.rowcount > 0

    def delete_student(self, student_id: int) -> bool:
        cursor = self.connection.execute(
            "DELETE FROM students WHERE student_id = ?", (student_id,)
        )
        return cursor.rowcount > 0

    def get_student_statistics(self) -> dict[str, Any]:
        row = self.connection.execute(
            """
            SELECT COUNT(*) AS student_count,
                   AVG(marks) AS average_marks,
                   MIN(marks) AS minimum_marks,
                   MAX(marks) AS maximum_marks
            FROM students
            """
        ).fetchone()
        return dict(row)

    def get_course_wise_statistics(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT c.course_id, c.course_name,
                   COUNT(s.student_id) AS student_count,
                   AVG(s.marks) AS average_marks
            FROM courses AS c
            LEFT JOIN students AS s ON s.course_id = c.course_id
            GROUP BY c.course_id, c.course_name
            ORDER BY c.course_name
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def get_courses_without_students(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT c.course_id, c.course_name
            FROM courses AS c
            LEFT JOIN students AS s ON s.course_id = c.course_id
            WHERE s.student_id IS NULL
            ORDER BY c.course_name
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def begin_transaction(self) -> None:
        if self.connection.in_transaction:
            raise RuntimeError("A transaction is already active.")
        self.connection.execute("BEGIN")

    def commit(self) -> None:
        if not self.connection.in_transaction:
            raise RuntimeError("There is no active transaction to commit.")
        self.connection.commit()

    def rollback(self) -> None:
        if not self.connection.in_transaction:
            raise RuntimeError("There is no active transaction to roll back.")
        self.connection.rollback()

    def transfer_student_course(
        self, student_id: int, new_course_id: int
    ) -> int:
        student = self.connection.execute(
            "SELECT course_id FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()
        if student is None:
            raise ValueError(f"Student {student_id} does not exist.")
        new_course = self.connection.execute(
            "SELECT course_id FROM courses WHERE course_id = ?", (new_course_id,)
        ).fetchone()
        if new_course is None:
            raise ValueError(f"Course {new_course_id} does not exist.")

        old_course_id = int(student["course_id"])
        if old_course_id == new_course_id:
            raise ValueError("The student is already enrolled in that course.")
        if self.connection.in_transaction:
            raise RuntimeError("Cannot transfer during another active transaction.")

        self.connection.execute("BEGIN IMMEDIATE")
        try:
            cursor = self.connection.execute(
                """
                UPDATE students
                SET course_id = ?
                WHERE student_id = ? AND course_id = ?
                """,
                (new_course_id, student_id, old_course_id),
            )
            if cursor.rowcount != 1:
                raise RuntimeError(
                    "The student's course changed during validation; transfer cancelled."
                )
            history_cursor = self.connection.execute(
                """
                INSERT INTO student_course_history
                    (student_id, old_course_id, new_course_id)
                VALUES (?, ?, ?)
                """,
                (student_id, old_course_id, new_course_id),
            )
            self.connection.commit()
            return int(history_cursor.lastrowid)
        except Exception:
            self.connection.rollback()
            raise

    def get_course_history(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT h.history_id, h.student_id, s.name AS student_name,
                   h.old_course_id, old_course.course_name AS old_course,
                   h.new_course_id, new_course.course_name AS new_course,
                   h.changed_at
            FROM student_course_history AS h
            JOIN students AS s ON s.student_id = h.student_id
            JOIN courses AS old_course ON old_course.course_id = h.old_course_id
            JOIN courses AS new_course ON new_course.course_id = h.new_course_id
            ORDER BY h.changed_at DESC, h.history_id DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def get_student_course_history(
        self, student_id: int
    ) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT h.history_id, h.student_id, s.name AS student_name,
                   h.old_course_id, old_course.course_name AS old_course,
                   h.new_course_id, new_course.course_name AS new_course,
                   h.changed_at
            FROM student_course_history AS h
            JOIN students AS s ON s.student_id = h.student_id
            JOIN courses AS old_course ON old_course.course_id = h.old_course_id
            JOIN courses AS new_course ON new_course.course_id = h.new_course_id
            WHERE h.student_id = ?
            ORDER BY h.changed_at DESC, h.history_id DESC
            """,
            (student_id,),
        ).fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        if self.connection.in_transaction:
            self.connection.rollback()
        self.connection.close()
