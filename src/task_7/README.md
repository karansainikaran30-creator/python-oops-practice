# SQL-PY-007: Database Transactions & ACID

Student Management System continuation with SQLite transactions and atomic
course transfers.

## Run

From this directory:

```powershell
python main.py
```

The database is created as `student_management.db` the first time the program
runs. Add course records (for example, BCA and MCA) before adding students or
transferring students. Course IDs are shown in the course list.

## Course transfers

Menu option **15** validates that the student and destination course exist and
that the student is not already in that course. The student update and history
insert are then performed within one `BEGIN IMMEDIATE` transaction. The method
commits only after both SQL statements succeed and rolls back on any exception.
Option **16** shows all transfer history or history for one student.

`begin_transaction()`, `commit()`, and `rollback()` are available for learning
explicit transaction boundaries. The connection enables SQLite foreign-key
checks.

## Tests

```powershell
python -m unittest -v
```

The simulated failure test creates a SQLite trigger that rejects history
insertion after the student update. It verifies that Rahul remains in BCA and
that no history record is committed.

## ACID notes

- **Atomicity:** the course update and history insert both commit, or both roll
  back.
- **Consistency:** foreign keys, unique email/course names, and value checks
  enforce valid data before and after changes.
- **Isolation:** `BEGIN IMMEDIATE` reserves SQLite's write transaction before
  applying the transfer.
- **Durability:** a successful SQLite commit persists the changes to the
  database file.

## Assignment SQL

```sql
UPDATE students SET course_id = ? WHERE student_id = ?;

INSERT INTO student_course_history
    (student_id, old_course_id, new_course_id)
VALUES (?, ?, ?);

SELECT h.history_id, s.name AS student_name,
       old_course.course_name AS old_course,
       new_course.course_name AS new_course, h.changed_at
FROM student_course_history AS h
JOIN students AS s ON s.student_id = h.student_id
JOIN courses AS old_course ON old_course.course_id = h.old_course_id
JOIN courses AS new_course ON new_course.course_id = h.new_course_id;
```
