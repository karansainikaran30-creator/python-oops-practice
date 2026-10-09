import sqlite3

from course import Course
from database import Database
from student import Student


def _read_marks(prompt):
    value = float(input(prompt))
    return int(value) if value.is_integer() else value


def _print_joined_students(students):
    if not students:
        print("No students found.")
        return
    print(f"{'ID':<6}{'Name':<20}{'Course':<16}{'Marks':>8}")
    print("-" * 50)
    for student in students:
        print(
            f"{student['student_id']:<6}{student['name']:<20}"
            f"{student['course_name']:<16}{student['marks']:>8g}"
        )


def _add_course(database):
    course = Course(int(input("Course ID: ")), input("Course name: "))
    if database.add_course(course):
        print("Course added successfully.")


def _view_courses(database):
    courses = database.get_all_courses()
    if not courses:
        print("No courses found.")
        return
    for course in courses:
        print(course)


def _add_student(database):
    student = Student(
        int(input("Student ID: ")),
        input("Name: "),
        int(input("Age: ")),
        int(input("Course ID: ")),
        _read_marks("Marks: "),
    )
    student.validate()
    if database.add_student(student):
        print("Student added successfully.")


def _search_student(database):
    student_id = int(input("Student ID: "))
    student = database.get_student_with_course_by_id(student_id)
    if student is None:
        print("Student not found.")
    else:
        _print_joined_students([student])


def _search_students_by_course(database):
    _print_joined_students(database.get_students_by_course(input("Course name: ")))


def _search_students_by_marks(database):
    _print_joined_students(database.get_students_by_marks(_read_marks("Minimum marks (0-100): ")))


def _sort_students(database):
    sort_by = input("Sort by marks or name: ").strip().lower()
    if sort_by not in ("marks", "name"):
        raise ValueError("Sort by marks or name only.")
    direction = input("Order (A)scending or (D)escending: ").strip().lower()
    if direction not in ("a", "d"):
        raise ValueError("Enter A for ascending or D for descending.")
    _print_joined_students(database.get_students_sorted(sort_by, desc=direction == "d"))


def _show_top_students(database):
    _print_joined_students(database.get_top_students(int(input("Number of top students: "))))


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
    course_input = input(f"Course ID [{student.course_id}]: ")
    course_id = int(course_input) if course_input else None
    marks_input = input(f"Marks [{student.marks:g}]: ")
    marks = float(marks_input) if marks_input else None
    if database.update_student(student_id, name=name, age=age, course_id=course_id, marks=marks):
        print("Student updated successfully.")
    else:
        print("Student not found.")


def _delete_student(database):
    student_id = int(input("Student ID to delete: "))
    student = database.get_student_with_course_by_id(student_id)
    if student is None:
        print("Student not found.")
        return
    _print_joined_students([student])
    if input("Delete this student? (y/n): ").strip().lower() != "y":
        print("Deletion cancelled.")
        return
    if database.delete_student(student_id):
        print("Student deleted successfully.")
    else:
        print("Student not found.")


def _show_student_statistics(database):
    stats = database.get_student_statistics()
    print(f"Total Students      : {stats['total_students']}")
    print(f"Total Marks         : {stats['total_marks']:g}")
    if stats["average_marks"] is None:
        print("Average Marks       : N/A")
        print("Highest Marks       : N/A")
        print("Lowest Marks        : N/A")
        return
    print(f"Average Marks       : {stats['average_marks']:.2f}")
    print(f"Highest Marks       : {stats['highest_marks']:g}")
    print(f"Lowest Marks        : {stats['lowest_marks']:g}")


def _show_course_statistics(database):
    statistics = database.get_course_statistics()
    if not statistics:
        print("No course statistics available.")
        return
    print(f"{'Course':<16}{'Students':>10}{'Average':>12}{'Highest':>12}{'Lowest':>10}")
    print("-" * 60)
    for row in statistics:
        average = f"{row['average_marks']:.2f}" if row["average_marks"] is not None else "N/A"
        highest = f"{row['highest_marks']:g}" if row["highest_marks"] is not None else "N/A"
        lowest = f"{row['lowest_marks']:g}" if row["lowest_marks"] is not None else "N/A"
        print(
            f"{row['course_name']:<16}{row['total_students']:>10}"
            f"{average:>12}{highest:>12}{lowest:>10}"
        )


def _show_courses_without_students(database):
    courses = database.get_courses_without_students()
    if not courses:
        print("Every course has at least one student.")
        return
    for course in courses:
        print(f"ID: {course['course_id']} | {course['course_name']}")


def main():
    database = Database()
    try:
        database.connect()
        database.create_course_table()
        database.create_table()
        actions = {
            "1": _add_course,
            "2": _view_courses,
            "3": _add_student,
            "4": lambda db: _print_joined_students(db.get_students_with_courses()),
            "5": _search_student,
            "6": _search_students_by_course,
            "7": _search_students_by_marks,
            "8": _sort_students,
            "9": _show_top_students,
            "10": _update_student,
            "11": _delete_student,
            "12": _show_student_statistics,
            "13": _show_course_statistics,
            "14": _show_courses_without_students,
        }

        while True:
            print(
                "\nStudent Management System\n"
                "1. Add Course\n"
                "2. View Courses\n"
                "3. Add Student\n"
                "4. View All Students\n"
                "5. Search Student\n"
                "6. Search Students by Course\n"
                "7. Search Students by Marks\n"
                "8. Sort Students\n"
                "9. Top N Students\n"
                "10. Update Student\n"
                "11. Delete Student\n"
                "12. Student Statistics\n"
                "13. Course-wise Statistics\n"
                "14. Courses Without Students\n"
                "15. Exit"
            )
            choice = input("Choose an option: ").strip()
            if choice == "15":
                print("Goodbye.")
                break
            action = actions.get(choice)
            if action is None:
                print("Invalid choice. Enter a number from 1 to 15.")
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