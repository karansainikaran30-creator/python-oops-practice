# SQL-PY-003: Student CRUD Operations

A beginner-friendly Python and SQLite application for creating, viewing, searching, updating, and deleting student records.

## Project files

- `main.py` runs the interactive menu.
- `student.py` defines a student and validates its fields.
- `database.py` owns the SQLite connection and CRUD queries.
- `student_management.db` is created automatically the first time the application runs.

## Run

From this folder, run:

```powershell
python main.py
```

The menu supports adding a student, listing all students, searching by ID, updating any combination of name/age/course/marks, and deleting a student after confirmation. Leave an update prompt blank to keep that field unchanged. Student IDs are primary keys and cannot be updated.

## Safety and validation

Student data is validated before insert and update, and the database also enforces `NOT NULL` and `CHECK` constraints. SQL values use placeholders. UPDATE and DELETE always include `WHERE student_id = ?`; update fields are chosen from a fixed allowlist. Database methods return `True` when one row is affected and `False` when no student matched. Database errors roll back changes and are reported by the menu.

## Required flow checks

1. Add ID 6, Karan, 20, BCA, 85, then view all students.
2. Search for ID 3.
3. Update ID 3's marks to 90.
4. Try marks of 150; validation should reject the update without changing the record.
5. Delete ID 6 and confirm with `y`.
6. Try deleting ID 100; the application reports that the student was not found.
7. Add a record, attempt to delete it, and answer `n`; it remains stored.

For automated checks, import `Database` and `Student` and pass a temporary file path to `Database`, so tests do not change the application's database.

## Assignment answers

1. CRUD means Create, Read, Update, and Delete.
2. `UPDATE` modifies existing records.
3. `DELETE` removes records.
4. `WHERE` restricts an operation to matching records.
5. In `DELETE`, `WHERE` prevents removing records other than the intended match.
6. An UPDATE without WHERE can modify every record in the table.
7. A DELETE without WHERE can delete every record in the table.
8. `student_id` is the primary key used to identify a record; changing it can break references and identity.
9. `cursor.rowcount` reports the number of rows affected by a statement.
10. Validation prevents invalid values from replacing valid stored data.
11. Confirmation helps prevent accidental data loss.
12. SELECT reads matching data; DELETE removes matching data.

## Viva review

- CRUD: Create, Read, Update, Delete.
- SQL commands for changing and removing records: `UPDATE` and `DELETE`.
- A `WHERE` clause narrows an operation to specific rows; omitting it can affect all rows.
- `student_id` remains unchanged because it is the primary key.