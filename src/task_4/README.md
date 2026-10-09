# SQL-PY-004: Student Filtering and Sorting

This Python and SQLite application continues the student CRUD system with course and marks filters, partial-name search, ascending/descending sorting, and a parameterized top-N query.

## Project files

- `main.py` runs the interactive 11-option menu.
- `student.py` defines and validates student records.
- `database.py` implements CRUD, filtering, AND/OR, sorting, and top-N queries.
- `student_management.db` is created automatically when the application first runs.

## Run

From this folder, run:

```powershell
python main.py
```

The menu retains all CRUD options from Task 3. For marks sorting, enter `A` for ascending or `D` for descending. Student deletion displays the record and requires `y` confirmation.

## Filtering and sorting methods

- `get_students_by_course(course)` selects exact course matches.
- `get_students_by_marks(min_marks)` selects students with marks greater than or equal to the minimum. The value must be from 0 to 100.
- `search_students_by_name(keyword)` uses `LIKE` and the pattern `f"%{keyword}%"` for partial matches.
- `get_students_sorted_by_marks(desc=True)` sorts from highest to lowest by default; pass `False` for lowest to highest.
- `get_students_sorted_by_name()` sorts alphabetically.
- `get_top_students(limit)` returns the highest-mark students; the limit must be a positive integer and is bound as a SQL parameter.
- `get_students_by_course_and_marks(course, min_marks)` demonstrates `AND`.
- `get_students_by_either_course(first_course, second_course)` demonstrates `OR`.

All user-provided SQL values are passed using placeholders. The sort direction is selected from fixed SQL keywords, not user-provided SQL text.

## Test checklist

1. Filter by `BCA`; every result should have course `BCA`.
2. Filter by minimum marks `80`; every result should have marks at least 80.
3. Search for `ri`; matching names should be returned.
4. Sort descending and ascending; check highest-to-lowest and lowest-to-highest order.
5. Request the top 3; no more than three records should be returned.
6. Minimum marks `150` raises `Invalid marks.` and is reported by the menu.
7. A top-N value of `-5` raises `Number of students must be greater than 0.`.
8. Use the AND method for BCA students with marks at least 80; use the OR method for BCA or BBA students.

For isolated tests, pass a temporary file path to `Database(db_path)` so the application database is unchanged.

## Assignment answers

1. `WHERE` filters rows to records matching a condition.
2. `AND` requires every condition to be true; `OR` requires at least one condition to be true.
3. `LIKE` compares text against a pattern, commonly for partial matching.
4. `%` matches any sequence of characters, including an empty sequence.
5. `ORDER BY` sorts query results by one or more columns.
6. `ASC` sorts ascending; `DESC` sorts descending.
7. `LIMIT` caps the number of rows returned.
8. Use `ORDER BY marks DESC LIMIT ?` and bind `5` as the parameter.
9. Use `WHERE marks > ?` and bind `80` (or use `>=` when including 80).
10. Use `WHERE name LIKE ?` and bind a pattern such as `%ri%`.
11. Without `ORDER BY`, result order is not guaranteed.
12. Parameterized SQL keeps input as data and helps prevent SQL injection and quoting errors.

## Viva review

- Find marks greater than 80 with `WHERE marks > ?` and a bound value of 80.
- Find the highest-mark student with `ORDER BY marks DESC LIMIT 1`.
- Search a partial name with `LIKE` and a `%keyword%` parameter.
- `ORDER BY marks ASC` lists low-to-high; `DESC` lists high-to-low.
- `LIMIT 5` returns at most five records.
- `WHERE` and `ORDER BY` can be combined, for example: `SELECT * FROM students WHERE course = ? ORDER BY marks DESC`.