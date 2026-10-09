"""PostgreSQL persistence and transaction handling."""

from typing import Any

import psycopg
from psycopg.rows import dict_row

from config import DatabaseConfig


class Database:
    def __init__(self, config: DatabaseConfig | None = None) -> None:
        self.config = config or DatabaseConfig.from_environment()
        self.connection: psycopg.Connection[dict[str, Any]] | None = None

    def connect(self) -> None:
        if self.connection is None or self.connection.closed:
            self.connection = psycopg.connect(
                host=self.config.host,
                port=self.config.port,
                dbname=self.config.database,
                user=self.config.user,
                password=self.config.password,
                row_factory=dict_row,
                autocommit=True,
            )

    def _connection(self) -> psycopg.Connection[dict[str, Any]]:
        if self.connection is None or self.connection.closed:
            raise RuntimeError("Database is not connected.")
        return self.connection

    def create_tables(self) -> None:
        self.execute_query(
            """
            CREATE TABLE IF NOT EXISTS courses (
                course_id SERIAL PRIMARY KEY,
                course_name VARCHAR(100) NOT NULL UNIQUE
            )
            """
        )
        self.execute_query(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INTEGER NOT NULL CHECK (age > 0),
                course_id INTEGER NOT NULL REFERENCES courses(course_id),
                marks NUMERIC(5, 2) NOT NULL CHECK (marks >= 0 AND marks <= 100)
            )
            """
        )
        self.execute_query(
            """
            CREATE TABLE IF NOT EXISTS student_course_history (
                history_id SERIAL PRIMARY KEY,
                student_id INTEGER NOT NULL REFERENCES students(student_id),
                old_course_id INTEGER NOT NULL REFERENCES courses(course_id),
                new_course_id INTEGER NOT NULL REFERENCES courses(course_id),
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def execute_query(
        self, query: str, parameters: tuple[Any, ...] | None = None
    ) -> int:
        with self._connection().cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.rowcount

    def fetch_one(
        self, query: str, parameters: tuple[Any, ...] | None = None
    ) -> dict[str, Any] | None:
        with self._connection().cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchone()

    def fetch_all(
        self, query: str, parameters: tuple[Any, ...] | None = None
    ) -> list[dict[str, Any]]:
        with self._connection().cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchall()

    def commit(self) -> None:
        self._connection().commit()

    def rollback(self) -> None:
        self._connection().rollback()

    def add_course(self, course_name: str) -> int:
        name = course_name.strip()
        if not name:
            raise ValueError("Course name cannot be empty.")
        row = self.fetch_one(
            "INSERT INTO courses (course_name) VALUES (%s) RETURNING course_id",
            (name,),
        )
        assert row is not None
        return int(row["course_id"])

    def get_courses(self) -> list[dict[str, Any]]:
        return self.fetch_all(
            "SELECT course_id, course_name FROM courses ORDER BY course_id"
        )

    def delete_course(self, course_id: int) -> bool:
        try:
            return self.execute_query(
                "DELETE FROM courses WHERE course_id = %s", (course_id,)
            ) > 0
        except psycopg.errors.ForeignKeyViolation as error:
            raise ValueError("Cannot delete a course that is in use or has history.") from error

    @staticmethod
    def _student_select() -> str:
        return """
            SELECT s.student_id, s.name, s.age, s.marks,
                   s.course_id, c.course_name
            FROM students AS s
            INNER JOIN courses AS c ON c.course_id = s.course_id
        """

    def add_student(
        self, student_id: int, name: str, age: int, marks: float, course_id: int
    ) -> int:
        self._validate_student(name, age, marks)
        self.execute_query(
            """
            INSERT INTO students (student_id, name, age, marks, course_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (student_id, name.strip(), age, marks, course_id),
        )
        return student_id

    @staticmethod
    def _validate_student(name: str, age: int, marks: float) -> None:
        if not name.strip():
            raise ValueError("Student name cannot be empty.")
        if age <= 0:
            raise ValueError("Age must be greater than zero.")
        if not 0 <= marks <= 100:
            raise ValueError("Marks must be between 0 and 100.")

    def get_all_students(self) -> list[dict[str, Any]]:
        return self.fetch_all(
            self._student_select() + " ORDER BY s.student_id"
        )

    def search_student(self, student_id: int) -> dict[str, Any] | None:
        return self.fetch_one(
            self._student_select() + " WHERE s.student_id = %s", (student_id,)
        )

    def search_students_by_course(self, course_id: int) -> list[dict[str, Any]]:
        return self.fetch_all(
            self._student_select()
            + " WHERE s.course_id = %s ORDER BY s.name, s.student_id",
            (course_id,),
        )

    def search_students_by_marks(
        self, minimum: float, maximum: float
    ) -> list[dict[str, Any]]:
        return self.fetch_all(
            self._student_select()
            + " WHERE s.marks BETWEEN %s AND %s"
            " ORDER BY s.marks DESC, s.student_id",
            (minimum, maximum),
        )

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
        return self.fetch_all(
            self._student_select()
            + f" ORDER BY {columns[order_by]} {direction}, s.student_id"
        )

    def top_n_students(self, count: int) -> list[dict[str, Any]]:
        if count <= 0:
            raise ValueError("The number of students must be positive.")
        return self.fetch_all(
            self._student_select()
            + " ORDER BY s.marks DESC, s.student_id LIMIT %s",
            (count,),
        )

    def update_student(
        self,
        student_id: int,
        name: str,
        age: int,
        marks: float,
        course_id: int,
    ) -> bool:
        self._validate_student(name, age, marks)
        return self.execute_query(
            """
            UPDATE students
            SET name = %s, age = %s, marks = %s, course_id = %s
            WHERE student_id = %s
            """,
            (name.strip(), age, marks, course_id, student_id),
        ) > 0

    def delete_student(self, student_id: int) -> bool:
        with self._connection().transaction():
            self.execute_query(
                "DELETE FROM student_course_history WHERE student_id = %s",
                (student_id,),
            )
            return self.execute_query(
                "DELETE FROM students WHERE student_id = %s", (student_id,)
            ) > 0

    def get_student_statistics(self) -> dict[str, Any]:
        row = self.fetch_one(
            """
            SELECT COUNT(*) AS student_count, AVG(marks) AS average_marks,
                   MIN(marks) AS minimum_marks, MAX(marks) AS maximum_marks
            FROM students
            """
        )
        assert row is not None
        return row

    def get_course_wise_statistics(self) -> list[dict[str, Any]]:
        return self.fetch_all(
            """
            SELECT c.course_id, c.course_name,
                   COUNT(s.student_id) AS student_count, AVG(s.marks) AS average_marks
            FROM courses AS c
            LEFT JOIN students AS s ON s.course_id = c.course_id
            GROUP BY c.course_id, c.course_name
            ORDER BY c.course_name
            """
        )

    def get_courses_without_students(self) -> list[dict[str, Any]]:
        return self.fetch_all(
            """
            SELECT c.course_id, c.course_name
            FROM courses AS c
            LEFT JOIN students AS s ON s.course_id = c.course_id
            WHERE s.student_id IS NULL
            ORDER BY c.course_name
            """
        )

    def begin_transaction(self) -> None:
        self._connection().execute("BEGIN")

    def transfer_student_course(
        self, student_id: int, new_course_id: int
    ) -> int:
        connection = self._connection()
        try:
            with connection.transaction():
                student = self.fetch_one(
                    "SELECT course_id FROM students WHERE student_id = %s FOR UPDATE",
                    (student_id,),
                )
                if student is None:
                    raise ValueError(f"Student {student_id} does not exist.")
                if self.fetch_one(
                    "SELECT course_id FROM courses WHERE course_id = %s",
                    (new_course_id,),
                ) is None:
                    raise ValueError(f"Course {new_course_id} does not exist.")

                old_course_id = int(student["course_id"])
                if old_course_id == new_course_id:
                    raise ValueError("The student is already enrolled in that course.")

                self.execute_query(
                    "UPDATE students SET course_id = %s WHERE student_id = %s",
                    (new_course_id, student_id),
                )
                history = self.fetch_one(
                    """
                    INSERT INTO student_course_history
                        (student_id, old_course_id, new_course_id)
                    VALUES (%s, %s, %s)
                    RETURNING history_id
                    """,
                    (student_id, old_course_id, new_course_id),
                )
                assert history is not None
                return int(history["history_id"])
        except ValueError:
            raise
        except Exception as error:
            raise RuntimeError(
                "Transaction failed. Rolling back changes."
            ) from error

    def get_course_history(self) -> list[dict[str, Any]]:
        return self.fetch_all(
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
        )

    def get_student_course_history(
        self, student_id: int
    ) -> list[dict[str, Any]]:
        return self.fetch_all(
            """
            SELECT h.history_id, h.student_id, s.name AS student_name,
                   h.old_course_id, old_course.course_name AS old_course,
                   h.new_course_id, new_course.course_name AS new_course,
                   h.changed_at
            FROM student_course_history AS h
            JOIN students AS s ON s.student_id = h.student_id
            JOIN courses AS old_course ON old_course.course_id = h.old_course_id
            JOIN courses AS new_course ON new_course.course_id = h.new_course_id
            WHERE h.student_id = %s
            ORDER BY h.changed_at DESC, h.history_id DESC
            """,
            (student_id,),
        )

    def close(self) -> None:
        if self.connection is not None and not self.connection.closed:
            self.connection.close()
