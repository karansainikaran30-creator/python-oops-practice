import sqlite3

from database import Database
from student import Student


def _parse_marks(raw_value):
    value = float(raw_value)
    return int(value) if value.is_integer() else value


def _read_marks(prompt):
    return _parse_marks(input(prompt))


def _display_student(student):
    if student is None:
        print("Student not found.")
    else:
        print(student)


def _add_student(database):
    student = Student(
        int(input("Student ID: ")),
        input("Name: "),
        int(input("Age: ")),
        input("Course: "),
        _read_marks("Marks: "),
    )
    student.validate()
    if database.add_student(student):
        print("Student added successfully.")


def _view_students(database):
    students = database.get_all_students()
    if not students:
        print("No students found.")
        return
    for student in students:
        print(student)


def _search_student(database):
    student = database.get_student_by_id(int(input("Student ID to search: ")))
    _display_student(student)


def _update_student(database):
    student_id = int(input("Student ID to update: "))
    student = database.get_student_by_id(student_id)
    if student is None:
        print("Student not found.")
        return

    print(f"Current record: {student}")
    print("Leave a field blank to keep its current value.")
    name = input(f"Name [{student.name}]: ") or None
    age_input = input(f"Age [{student.age}]: ")
    age = int(age_input) if age_input else None
    course = input(f"Course [{student.course}]: ") or None
    marks_input = input(f"Marks [{student.marks:g}]: ")
    marks = _parse_marks(marks_input) if marks_input else None

    if database.update_student(student_id, name=name, age=age, course=course, marks=marks):
        print("Student updated successfully.")
    else:
        print("Student not found.")


def _delete_student(database):
    student_id = int(input("Student ID to delete: "))
    student = database.get_student_by_id(student_id)
    if student is None:
        print("Student not found.")
        return

    print(f"Student to delete: {student}")
    confirmation = input("Delete this student? (y/n): ").strip().lower()
    if confirmation != "y":
        print("Deletion cancelled.")
        return

    if database.delete_student(student_id):
        print("Student deleted successfully.")
    else:
        print("Student not found.")


def main():
    database = Database()
    try:
        database.connect()
        database.create_table()
        actions = {
            "1": _add_student,
            "2": _view_students,
            "3": _search_student,
            "4": _update_student,
            "5": _delete_student,
        }

        while True:
            print(
                "\nStudent Management System\n"
                "1. Add Student\n"
                "2. View All Students\n"
                "3. Search Student\n"
                "4. Update Student\n"
                "5. Delete Student\n"
                "6. Exit"
            )
            choice = input("Choose an option: ").strip()
            if choice == "6":
                print("Goodbye.")
                break
            action = actions.get(choice)
            if action is None:
                print("Invalid choice. Enter a number from 1 to 6.")
                continue
            try:
                action(database)
            except (ValueError, sqlite3.Error) as error:
                print(f"Error: {error}")
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        database.close()


if __name__ == "__main__":
    main()