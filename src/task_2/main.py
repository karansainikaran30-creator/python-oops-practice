import sqlite3

from database import Database, DuplicateStudentError
from student import Student


def display_student(row):
    print(Student(*row))


def add_student(database):
    try:
        student_id = int(input("Student ID: "))
    except ValueError:
        print("Validation error: Student ID must be an integer.")
        return

    name = input("Name: ")
    try:
        age = int(input("Age: "))
    except ValueError:
        print("Validation error: Age must be an integer greater than 0.")
        return

    course = input("Course: ")
    try:
        marks = float(input("Marks: "))
    except ValueError:
        print("Validation error: Marks must be a number between 0 and 100.")
        return

    try:
        student = Student(student_id, name, age, course, marks)
        database.add_student(student)
        print("Student added successfully.")
    except DuplicateStudentError as error:
        print(error)
    except ValueError as error:
        print(f"Validation error: {error}")


def search_student(database):
    try:
        student_id = int(input("Student ID to search: "))
    except ValueError:
        print("Validation error: Student ID must be an integer.")
        return

    row = database.get_student_by_id(student_id)
    if row is None:
        print("Student not found.")
    else:
        display_student(row)


def run_menu(database):
    while True:
        print("\nUniversity Student Management System")
        print("1. Add student")
        print("2. Show all students")
        print("3. Search student by ID")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student(database)
        elif choice == "2":
            students = database.get_all_students()
            if not students:
                print("No students found.")
            else:
                for row in students:
                    display_student(row)
        elif choice == "3":
            search_student(database)
        elif choice == "4":
            print("Database connection closed. Goodbye.")
            return
        else:
            print("Please choose an option from 1 to 4.")


def main():
    database = Database()
    try:
        database.connect()
        database.create_table()
        run_menu(database)
    except sqlite3.Error:
        print("Database error: unable to complete the requested operation.")
    finally:
        database.close()


if __name__ == "__main__":
    main()