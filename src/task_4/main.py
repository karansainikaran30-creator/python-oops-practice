import sqlite3

from database import Database
from student import Student


def _parse_marks(raw_value):
    value = float(raw_value)
    return int(value) if value.is_integer() else value


def _read_marks(prompt):
    return _parse_marks(input(prompt))


def _print_students(students):
    if not students:
        print("No students found.")
        return
    for student in students:
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


def _search_student_by_id(database):
    student = database.get_student_by_id(int(input("Student ID: ")))
    _print_students([student] if student else [])


def _search_student_by_course(database):
    course = input("Course: ")
    _print_students(database.get_students_by_course(course))


def _search_student_by_name(database):
    keyword = input("Name keyword: ")
    _print_students(database.search_students_by_name(keyword))


def _filter_students_by_marks(database):
    min_marks = _read_marks("Minimum marks (0-100): ")
    _print_students(database.get_students_by_marks(min_marks))


def _sort_students_by_marks(database):
    direction = input("Sort marks (A)scending or (D)escending? ").strip().lower()
    if direction not in ("a", "d"):
        raise ValueError("Enter A for ascending or D for descending.")
    _print_students(database.get_students_sorted_by_marks(desc=direction == "d"))


def _show_top_students(database):
    limit = int(input("Number of top students: "))
    _print_students(database.get_top_students(limit))


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
    if input("Delete this student? (y/n): ").strip().lower() != "y":
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
            "2": lambda db: _print_students(db.get_all_students()),
            "3": _search_student_by_id,
            "4": _search_student_by_course,
            "5": _search_student_by_name,
            "6": _filter_students_by_marks,
            "7": _sort_students_by_marks,
            "8": _show_top_students,
            "9": _update_student,
            "10": _delete_student,
        }

        while True:
            print(
                "\nStudent Management System\n"
                "1. Add Student\n"
                "2. View All Students\n"
                "3. Search Student by ID\n"
                "4. Search Student by Course\n"
                "5. Search Student by Name\n"
                "6. Filter Students by Marks\n"
                "7. Sort Students by Marks\n"
                "8. Top N Students\n"
                "9. Update Student\n"
                "10. Delete Student\n"
                "11. Exit"
            )
            choice = input("Choose an option: ").strip()
            if choice == "11":
                print("Goodbye.")
                break
            action = actions.get(choice)
            if action is None:
                print("Invalid choice. Enter a number from 1 to 11.")
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