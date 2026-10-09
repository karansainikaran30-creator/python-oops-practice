import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from database import Database
from main import add_student, search_student
from student import Student


class StudentManagementTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        database_path = Path(self.temp_directory.name) / "students.db"
        self.database = Database(str(database_path))
        self.database.connect()
        self.database.create_table()

    def tearDown(self):
        self.database.close()
        self.temp_directory.cleanup()

    def run_with_input(self, function, answers):
        output = StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output):
            function(self.database)
        return output.getvalue()

    def test_valid_insert_and_duplicate_id_message(self):
        self.database.add_student(Student(1, "Rahul", 20, "BCA", 82))
        output = self.run_with_input(
            add_student, ["6", "Karan", "20", "BCA", "85"]
        )
        self.assertIn("Student added successfully.", output)
        self.assertEqual(
            self.database.get_student_by_id(6),
            (6, "Karan", 20, "BCA", 85.0),
        )

        output = self.run_with_input(
            add_student, ["1", "Another Student", "20", "BCA", "75"]
        )
        self.assertIn("Student ID already exists.", output)
        self.assertNotIn("Traceback", output)
        self.assertEqual(len(self.database.get_all_students()), 2)

    def test_python_validation_messages(self):
        invalid_inputs = [
            (["7", "Karan", "-5", "BCA", "85"], "Age must be an integer greater than 0."),
            (["7", "Karan", "20", "BCA", "150"], "Marks must be between 0 and 100."),
            (["7", "", "20", "BCA", "85"], "Student name cannot be empty."),
            (["7", "Karan", "20", "", "85"], "Course cannot be empty."),
        ]
        for answers, expected_message in invalid_inputs:
            with self.subTest(expected_message=expected_message):
                output = self.run_with_input(add_student, answers)
                self.assertIn(expected_message, output)
                self.assertEqual(self.database.get_all_students(), [])

    def test_database_constraints_reject_invalid_values(self):
        invalid_rows = [
            (1, None, 20, "BCA", 80),
            (1, "Student", None, "BCA", 80),
            (1, "Student", 20, None, 80),
            (1, "Student", 20, "BCA", None),
            (1, "Student", -5, "BCA", 80),
            (1, "Student", 20, "BCA", 150),
        ]
        for row in invalid_rows:
            with self.subTest(row=row):
                with self.assertRaises(sqlite3.IntegrityError):
                    self.database.connection.execute(
                        "INSERT INTO students VALUES (?, ?, ?, ?, ?)", row
                    )
                self.database.connection.rollback()

        columns = {
            row[1]: row
            for row in self.database.connection.execute(
                "PRAGMA table_info(students)"
            )
        }
        self.assertEqual(columns["student_id"][5], 1)
        for name in ("name", "age", "course", "marks"):
            self.assertEqual(columns[name][3], 1)

    def test_search_existing_and_missing_students(self):
        self.database.add_student(Student(6, "Karan", 20, "BCA", 85))
        output = self.run_with_input(search_student, ["6"])
        self.assertIn("Karan", output)

        output = self.run_with_input(search_student, ["99"])
        self.assertIn("Student not found.", output)

    def test_committed_record_survives_reconnecting(self):
        self.database.add_student(Student(6, "Karan", 20, "BCA", 85))
        database_path = self.database.database_path
        self.database.close()
        self.database = Database(database_path)
        self.database.connect()
        self.assertIsNotNone(self.database.get_student_by_id(6))


if __name__ == "__main__":
    unittest.main()