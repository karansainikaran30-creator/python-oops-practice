# University Student Management System

**Task ID:** SQL-PY-001

## Problem

Store university student records persistently in SQLite, rather than losing data when a Python program exits. The application can add a student, list saved students, and search by student ID.

## Technologies

- Python 3
- SQLite, accessed through Python's built-in `sqlite3` module
- SQL: `CREATE TABLE`, `INSERT`, and `SELECT` with `WHERE`

## Project files

- `main.py` runs the interactive application.
- `student.py` defines and validates the `Student` class.
- `database.py` connects to SQLite and performs database operations.
- `student_management.db` is created in the current working directory when the application runs.

## Database table

The `students` table stores `student_id` (`INTEGER`), `name` (`TEXT`), `age` (`INTEGER`), `course` (`TEXT`), and `marks` (`REAL`). The task's introductory schema is used; primary keys and additional SQL constraints are left for the SQL-PY-002 progression.

## Run

From this directory, run:

```text
python main.py
```

Choose **1** to add a student, **2** to list all students, **3** to search by ID, or **4** to exit. The database table is created automatically if it does not exist. Records remain in the database between runs.

## How Python communicates with SQL

`sqlite3.connect()` opens the database file and returns a connection. The application executes SQL through that connection. Adding a student uses `INSERT INTO` with `?` placeholders, then calls `commit()` so the change is saved. Listing uses `SELECT`; searching uses `SELECT ... WHERE student_id = ?`. The connection is closed when the application exits.

## Validation and errors

- Student ID must be an integer.
- Name and course must not be empty.
- Age must be an integer greater than 0.
- Marks must be a number from 0 through 100.
- Invalid student input is rejected before an insert. A missing search result displays `Student not found.` Database errors are displayed, and the connection is closed in the `finally` block.

## Test cases

| Test | Expected result |
| --- | --- |
| Add a valid student | Student is stored successfully and can be retrieved. |
| Search for an existing ID | The matching student is displayed. |
| Search for a missing ID | `Student not found.` is displayed. |
| Enter a negative age | Validation error; no record is inserted. |
| Enter marks above 100 | Validation error; no record is inserted. |
| Enter an empty name | Validation error; no record is inserted. |

## Assignment questions

1. A Python object is an in-memory instance with fields and behavior; a database record is structured data stored persistently in a table.
2. A list disappears when its program ends and is difficult to share or query reliably. A database persists data and supports structured queries.
3. SQL (Structured Query Language) is used to define, read, and change data in relational databases.
4. `sqlite3.connect()` opens a connection to an SQLite database file, creating the file if it does not exist.
5. `cursor.execute()` sends a SQL statement and any bound values to the database for execution.
6. `commit()` saves a transaction's changes so they persist after the connection closes.
7. A Python class defines application behavior and object fields; an SQL table defines the columns and rows used to store records.
8. Validation prevents invalid values from entering persistent storage and causing inconsistent data.

## Sample records

Use the **Add student** menu option to enter the sample records from the task: Rahul (ID 1, age 20, BCA, 82), Priya (ID 2, age 21, BCA, 88), Amit (ID 3, age 20, BBA, 76), Neha (ID 4, age 22, BCA, 91), and Rohit (ID 5, age 21, BBA, 69).