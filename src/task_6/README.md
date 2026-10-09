# SQL-PY-006: Student Relationships and JOINs

This project models courses and students as related tables. Each student stores a `course_id` foreign key rather than repeating a course name. One course can have many students.

## Project files

- `main.py` provides the 15-option application menu.
- `database.py` creates and queries the related tables.
- `student.py` defines student records with `course_id`.
- `course.py` defines and validates course records.
- `student_management.db` is created automatically on first run.

## Run

From this folder, run:

```powershell
python main.py
```

Add courses before adding students. Student course IDs are checked before insertion, and SQLite foreign-key enforcement provides a second integrity check. A course with enrolled students cannot be deleted. Delete the students first if removing that course is intended.

## JOIN and analytics methods

- `get_students_with_courses()` uses `INNER JOIN` and table aliases to show each student with the course name.
- `get_students_by_course(course_name)` filters joined rows by course.
- `get_students_by_marks(min_marks)`, `get_students_sorted(...)`, and `get_top_students(limit)` preserve the previous filtering and sorting workflows.
- `get_course_statistics()` uses `LEFT JOIN`, `COUNT`, `AVG`, `MAX`, `MIN`, and `GROUP BY`, so courses with no students remain visible.
- `get_courses_without_students()` uses `LEFT JOIN` and `WHERE s.student_id IS NULL`.
- `get_student_statistics()` performs student-level aggregate calculations in SQLite.

## Test checklist

1. Add BCA, BBA, MCA, and MBA.
2. Add Rahul, Priya, and Neha to BCA; Amit and Rohit to BBA.
3. Try adding a student with course ID 99; it must report `Invalid course ID.` and insert nothing.
4. View all students and verify the joined course names.
5. Verify MCA and MBA remain in course statistics with zero students and `N/A` mark values.
6. Verify the courses-without-students option returns MCA and MBA.
7. Check counts and mark aggregates for BCA and BBA.

For isolated checks, pass a temporary database path to `Database(db_path)`.

## Assignment answers

1. A foreign key refers to a key in another table and enforces a valid relationship.
2. A primary key uniquely identifies a row in its table.
3. A relationship connects records across tables using related keys.
4. One-to-many means one course can be related to multiple student records.
5. A separate course table avoids repeated names and keeps course data consistent.
6. Normalization organizes data to reduce duplication and update anomalies.
7. `INNER JOIN` returns rows with matching keys in both tables.
8. `LEFT JOIN` returns every left-table row and any matching right-table rows.
9. An INNER JOIN excludes unmatched rows; a LEFT JOIN preserves unmatched left rows with NULL right-side values.
10. `ON` specifies how rows in the joined tables match.
11. Aliases make queries shorter and clarify which table each column comes from.
12. The foreign-key constraint rejects a student row that references a missing course.
13. LEFT JOIN returns NULL for right-table columns when no matching row exists.
14. LEFT JOIN courses to students and filter where `students.student_id IS NULL`.
15. Yes. JOIN combines related rows, and GROUP BY then aggregates them by a chosen key.

## Viva review

- A foreign key links a record to a key in another table.
- INNER JOIN returns matching student/course records; LEFT JOIN also retains unmatched courses.
- Find courses without students with LEFT JOIN and `WHERE s.student_id IS NULL`.
- A separate courses table avoids repeating course names; one course can have many students.