"""Command-line interface for the PostgreSQL student management system."""

from collections.abc import Callable
from typing import Any

import psycopg

from config import DatabaseConfig
from database import Database


def display_rows(rows: list[dict[str, Any]]) -> None:
    if not rows:
        print("No records found.")
        return
    for row in rows:
        print(" | ".join(f"{key}: {value}" for key, value in row.items()))


def _prompt_student_fields() -> tuple[int, str, int, float, int]:
    return (
        int(input("Student ID: ")),
        input("Student name: ").strip(),
        int(input("Age: ")),
        float(input("Marks (0-100): ")),
        int(input("Course ID: ")),
    )


def run_menu(database: Database) -> None:
    actions: dict[str, Callable[[], None]] = {
        "1": lambda: print(
            f"Course added with ID {database.add_course(input('Course name: '))}."
        ),
        "2": lambda: display_rows(database.get_courses()),
        "3": lambda: print(
            f"Student added with ID {database.add_student(*_prompt_student_fields())}."
        ),
        "4": lambda: display_rows(database.get_all_students()),
        "5": _search_student_action(database),
        "6": lambda: display_rows(
            database.search_students_by_course(int(input("Course ID: ")))
        ),
        "7": _search_marks_action(database),
        "8": _sort_students_action(database),
        "9": lambda: display_rows(
            database.top_n_students(int(input("How many top students? ")))
        ),
        "10": _update_student_action(database),
        "11": lambda: _delete_student(database),
        "12": lambda: print(database.get_student_statistics()),
        "13": lambda: display_rows(database.get_course_wise_statistics()),
        "14": lambda: display_rows(database.get_courses_without_students()),
        "15": lambda: _transfer_student(database),
        "16": _course_history_action(database),
        "17": lambda: _delete_course(database),
    }
    while True:
        print(
            "\n1. Add Course\n2. View Courses\n3. Add Student\n"
            "4. View All Students\n5. Search Student\n"
            "6. Search Students by Course\n7. Search Students by Marks\n"
            "8. Sort Students\n9. Top N Students\n10. Update Student\n"
            "11. Delete Student\n12. Student Statistics\n"
            "13. Course-wise Statistics\n14. Courses Without Students\n"
            "15. Transfer Student Course\n16. View Course Transfer History\n"
            "17. Delete Course\n18. Exit"
        )
        choice = input("Choose an option: ").strip()
        if choice == "18":
            return
        action = actions.get(choice)
        if action is None:
            print("Invalid menu choice.")
            continue
        try:
            action()
        except ValueError as error:
            print(f"Invalid input: {error}")
        except psycopg.errors.UniqueViolation as error:
            constraint = error.diag.constraint_name if error.diag else None
            if constraint == "students_pkey":
                print("Student ID already exists.")
            elif constraint == "courses_course_name_key":
                print("Course already exists.")
            else:
                print("A record with that unique value already exists.")
        except psycopg.errors.ForeignKeyViolation:
            print("Invalid course ID, or the record is still in use.")
        except psycopg.Error as error:
            print(f"Database operation failed: {error.sqlstate or error.__class__.__name__}.")
        except RuntimeError as error:
            print(error)


def _search_student_action(database: Database) -> Callable[[], None]:
    def action() -> None:
        student = database.search_student(int(input("Student ID: ")))
        if student is None:
            print("Student not found.")
        else:
            display_rows([student])

    return action


def _search_marks_action(database: Database) -> Callable[[], None]:
    def action() -> None:
        minimum = float(input("Minimum marks: "))
        maximum = float(input("Maximum marks: "))
        if minimum > maximum:
            raise ValueError("Minimum marks cannot exceed maximum marks.")
        display_rows(database.search_students_by_marks(minimum, maximum))

    return action


def _sort_students_action(database: Database) -> Callable[[], None]:
    def action() -> None:
        field = input("Sort by student_id, name, age, marks, or course: ").strip()
        descending = input("Descending order? (y/n): ").strip().lower() == "y"
        display_rows(database.sort_students(field, descending))

    return action


def _update_student_action(database: Database) -> Callable[[], None]:
    def action() -> None:
        student_id, name, age, marks, course_id = _prompt_student_fields()
        if database.update_student(student_id, name, age, marks, course_id):
            print("Student updated.")
        else:
            print("Student not found.")

    return action


def _delete_student(database: Database) -> None:
    student_id = int(input("Student ID to delete: "))
    if database.delete_student(student_id):
        print("Student deleted.")
    else:
        print("Student not found.")


def _delete_course(database: Database) -> None:
    course_id = int(input("Course ID to delete: "))
    if database.delete_course(course_id):
        print("Course deleted.")
    else:
        print("Course not found.")


def _transfer_student(database: Database) -> None:
    student_id = int(input("Student ID: "))
    new_course_id = int(input("New course ID: "))
    history_id = database.transfer_student_course(student_id, new_course_id)
    print(f"Course transfer committed (history ID {history_id}).")


def _course_history_action(database: Database) -> Callable[[], None]:
    def action() -> None:
        student_id = input("Student ID, or press Enter for all history: ").strip()
        if student_id:
            display_rows(database.get_student_course_history(int(student_id)))
        else:
            display_rows(database.get_course_history())

    return action


def _connection_error_message(error: psycopg.OperationalError) -> str:
    if getattr(error, "sqlstate", None) == "28P01":
        return "Database authentication failed."
    return "Unable to connect to database."


def main() -> None:
    try:
        database = Database(DatabaseConfig.from_environment())
    except ValueError as error:
        print(f"Database configuration error: {error}")
        return

    try:
        database.connect()
        print("Successfully connected to PostgreSQL.")
        database.create_tables()
    except psycopg.OperationalError as error:
        print(_connection_error_message(error))
        database.close()
        return
    except psycopg.Error as error:
        print(f"Unable to initialize database: {error.sqlstate or error.__class__.__name__}.")
        database.close()
        return

    try:
        run_menu(database)
    finally:
        database.close()


if __name__ == "__main__":
    main()
