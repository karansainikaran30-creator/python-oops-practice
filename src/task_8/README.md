# SQL-PY-008: PostgreSQL Student Management System

This project continues the student management application from SQL-PY-007,
migrating its persistence layer from SQLite to PostgreSQL. Python remains the
application layer; PostgreSQL stores and validates the relational data.

## Requirements

- Python 3.10 or newer
- PostgreSQL server
- A PostgreSQL database named `student_management`

Create the database once from `psql` or pgAdmin:

```sql
CREATE DATABASE student_management;
```

The application creates the `courses`, `students`, and
`student_course_history` tables on startup if they do not exist. Courses receive
an automatically generated `SERIAL` ID. Student IDs are entered by the user,
matching the assignment's `INTEGER PRIMARY KEY` definition.

## Setup

From this directory, install the Python packages:

```powershell
python -m pip install -r requirements.txt
```

Edit `.env` with the host, port, database name, user, and password for your
PostgreSQL server. The included password is only a placeholder; replace it
before running the application. `.env` is excluded by `.gitignore`.

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=student_management
DB_USER=postgres
DB_PASSWORD=your_actual_password
```

Start the application:

```powershell
python main.py
```

The app reports a concise message for unavailable PostgreSQL servers and
authentication failures. It never embeds the password in Python source.

## Features

- Create, list, and delete courses; add, list, search, update, and delete students.
- Search by course or mark range, sort by supported fields, and display the top
  students and aggregate statistics.
- Student/course results use an `INNER JOIN`.
- Transfer a student between courses in a single PostgreSQL transaction:
  lock the student row, update the course, insert transfer history, and commit.
  An exception rolls back both changes.
- All values are passed through psycopg parameterized queries (`%s`). The only
  interpolated SQL fragments are selected from fixed, allow-listed sort columns
  and directions.

Deleting a student also removes that student's transfer-history rows in the
same transaction, since history rows reference students and the assignment's
foreign key does not specify cascading deletes. A course cannot be deleted
while referenced by students or transfer history.

## Verification checklist

1. Start PostgreSQL and run `python main.py`; confirm the successful connection
   message.
2. Inspect the `student_management` database and verify all three tables exist.
3. Add BCA, BBA, MCA, and MBA; then add at least five students.
4. Use **View All Students** to check the joined student, course, and marks data.
5. Search, update, delete, and transfer a student; inspect course-transfer history.
6. To verify rollback, temporarily make the history insert fail (for example,
   with a PostgreSQL trigger), try a course transfer, then verify the student's
   original course remains and no history row was added. Remove the temporary
   trigger afterward.
7. Exit and restart the application; verify committed data remains.

## Assignment SQL examples

```sql
CREATE TABLE IF NOT EXISTS courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO students (student_id, name, age, course_id, marks)
VALUES (1001, 'Asha', 20, 1, 91.50);

UPDATE students SET marks = 95.00 WHERE student_id = 1001;

DELETE FROM students WHERE student_id = 1001;

SELECT s.student_id, s.name, c.course_name, s.marks
FROM students AS s
INNER JOIN courses AS c ON c.course_id = s.course_id;

SELECT student_id, name, marks
FROM students
ORDER BY marks DESC
LIMIT 3;
```

## Concepts

- **PostgreSQL** is an open-source, client-server relational database system.
- A database server hosts databases and handles client connections and SQL.
  Python is the client application; psycopg is its PostgreSQL driver.
- A cursor executes SQL and reads the result rows. A connection represents the
  session with the server and controls transactions.
- `VARCHAR` stores bounded text and `NUMERIC` stores exact decimal values, which
  is appropriate for marks. `SERIAL` supplies generated integer course and
  history IDs.
- Environment variables keep credentials out of source code. Parameterized
  queries prevent user-provided values from being interpreted as SQL syntax,
  mitigating SQL injection.
- Transactions make the student-course update and history insertion atomic.
  PostgreSQL foreign keys preserve referential integrity.
