# Robust Student Database with Constraints

**Task ID:** SQL-PY-002

## Problem

Continue the Student Management System with a SQLite schema that enforces data integrity even if a database write bypasses the Python application-level checks.

## Technologies

- Python 3
- SQLite through the built-in `sqlite3` module
- SQL `CREATE TABLE`, `INSERT`, and `SELECT ... WHERE`

## Project files

- `main.py` provides the interactive application.
- `student.py` defines the `Student` class and validates student data.
- `database.py` owns the connection, constrained schema, inserts, searches, and transaction handling.
- `student_management.db` is created in this directory when the application runs.

## Database design

| Column | Type | Constraint |
| --- | --- | --- |
| `student_id` | `INTEGER` | `PRIMARY KEY` |
| `name` | `TEXT` | `NOT NULL` |
| `age` | `INTEGER` | `NOT NULL`, `CHECK (age > 0)` |
| `course` | `TEXT` | `NOT NULL` |
| `marks` | `REAL` | `NOT NULL`, `CHECK (marks >= 0 AND marks <= 100)` |

The optional `status DEFAULT 'ACTIVE'` column and optional course-name `CHECK` are not part of the required schema in this task.

## Run

From this directory, run:

```text
python main.py
```

Choose **1** to add a student, **2** to list all students, **3** to search by ID, or **4** to exit. The table is created automatically if it does not exist.

Run the automated tests from this directory with:

```text
python -m unittest -v
```

## Validation and transactions

Python validation provides immediate, readable feedback: ID and age must be integers, name and course must not be blank, age must be positive, and marks must be between 0 and 100. SQLite independently enforces primary-key uniqueness, required non-NULL fields, positive age, and the marks range. An empty string is different from `NULL`, so blank names and courses are rejected by the Python validation.

Inserts use bound parameters. A successful insert is committed. A failed insert is rolled back; a duplicate ID is reported as `Student ID already exists.` Other database errors are handled without exposing raw SQLite details to the user. The connection is closed when the application exits.

## Test cases

| Test | Expected result |
| --- | --- |
| Add ID 6, Karan, 20, BCA, 85 | Student added successfully. |
| Add an ID already in the table | Student ID already exists. |
| Enter age -5 | Age validation error; no row is inserted. |
| Enter marks 150 | Marks validation error; no row is inserted. |
| Enter an empty name | Student name cannot be empty. |
| Enter an empty course | Course validation error; no row is inserted. |
| Search for an existing student | The matching record is displayed. |
| Search for an unknown ID | Student not found. |

All five automated test methods pass, covering these cases, the database constraints, and persistence after reconnecting.

## Viva questions

1. A primary key is a column (or column set) that uniquely identifies each row.
2. `student_id` is the identifier used to find one student and reject duplicate records.
3. No. A primary key must be unique and cannot be `NULL`.
4. `NOT NULL` prevents a column from being stored without a value.
5. `CHECK` rejects values that do not satisfy a condition, such as `age > 0`.
6. Constraints protect the database when writes come from code that skips Python validation.
7. SQLite rejects a repeated primary key; the application translates that into `Student ID already exists.`
8. `NULL` means a value is absent; an empty string is a text value containing no characters.
9. `DEFAULT` supplies a column value when an insert omits it. It is an optional extension here.
10. Enforce data integrity in both Python and the database: Python helps the user, while the database protects persisted records.