"""Tests for transfer validation and transaction atomicity."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from database import Database


class CourseTransferTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Database(Path(self.temp_dir.name) / "test.db")
        self.bca_id = self.database.add_course("BCA")
        self.mca_id = self.database.add_course("MCA")
        self.student_id = self.database.add_student(
            "Rahul", 20, "rahul@example.com", 85, self.bca_id
        )

    def tearDown(self) -> None:
        self.database.close()
        self.temp_dir.cleanup()

    def test_successful_transfer_updates_student_and_history(self) -> None:
        history_id = self.database.transfer_student_course(
            self.student_id, self.mca_id
        )

        self.assertGreater(history_id, 0)
        self.assertEqual(
            self.database.search_student(self.student_id)["course_id"], self.mca_id
        )
        history = self.database.get_student_course_history(self.student_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["old_course_id"], self.bca_id)
        self.assertEqual(history[0]["new_course_id"], self.mca_id)

    def test_invalid_student_does_not_change_data(self) -> None:
        with self.assertRaisesRegex(ValueError, "does not exist"):
            self.database.transfer_student_course(999, self.mca_id)
        self.assertEqual(
            self.database.search_student(self.student_id)["course_id"], self.bca_id
        )
        self.assertEqual(self.database.get_course_history(), [])

    def test_invalid_course_does_not_change_data(self) -> None:
        with self.assertRaisesRegex(ValueError, "does not exist"):
            self.database.transfer_student_course(self.student_id, 99)
        self.assertEqual(
            self.database.search_student(self.student_id)["course_id"], self.bca_id
        )
        self.assertEqual(self.database.get_course_history(), [])

    def test_same_course_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "already enrolled"):
            self.database.transfer_student_course(self.student_id, self.bca_id)
        self.assertEqual(
            self.database.search_student(self.student_id)["course_id"], self.bca_id
        )
        self.assertEqual(self.database.get_course_history(), [])

    def test_history_failure_rolls_back_student_update(self) -> None:
        self.database.connection.execute(
            """
            CREATE TRIGGER fail_history_insert
            BEFORE INSERT ON student_course_history
            BEGIN
                SELECT RAISE(ABORT, 'simulated history failure');
            END
            """
        )

        with self.assertRaisesRegex(sqlite3.IntegrityError, "simulated history failure"):
            self.database.transfer_student_course(self.student_id, self.mca_id)

        self.assertFalse(self.database.connection.in_transaction)
        self.assertEqual(
            self.database.search_student(self.student_id)["course_id"], self.bca_id
        )
        self.assertEqual(self.database.get_course_history(), [])

    def test_explicit_transaction_methods(self) -> None:
        self.database.begin_transaction()
        self.database.connection.execute(
            "UPDATE students SET marks = 90 WHERE student_id = ?",
            (self.student_id,),
        )
        self.database.rollback()
        self.assertEqual(self.database.search_student(self.student_id)["marks"], 85)


if __name__ == "__main__":
    unittest.main()
