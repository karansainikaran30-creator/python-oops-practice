# SQL-PY-005: Student Performance Analytics

This Python and SQLite application carries forward student CRUD, filtering, and sorting, and adds SQL-side student and course analytics with aggregate functions, `GROUP BY`, and `HAVING`.

## Project files

- `main.py` runs the 13-option menu.
- `student.py` defines and validates student records.
- `database.py` contains the CRUD, filtering, sorting, and analytics queries.
- `student_management.db` is created automatically on the first run.

## Run

From this folder, run:

```powershell
python main.py
```

Menu option 11 displays student count, total and average marks, and highest and lowest marks. Option 12 displays course-wise count, average, highest, and lowest marks. Empty databases display a count of zero, a total of zero, and `N/A` for undefined mark statistics.

## Analytics methods

- `get_total_students()`, `get_total_marks()`, `get_average_marks()`, `get_highest_marks()`, and `get_lowest_marks()` each use SQL aggregate functions.
- `get_student_statistics()` gets all student-level measures in one SQL aggregate query for the menu.
- `get_course_statistics()` calculates `COUNT`, `AVG`, `MAX`, and `MIN` together using `GROUP BY course`.
- `get_course_average_marks()`, `get_course_highest_marks()`, and `get_course_lowest_marks()` expose each course aggregate separately.
- `get_courses_above_average(min_average)` uses `GROUP BY` and `HAVING AVG(marks) >= ?`.

Previous filtering, sorting, top-N, AND/OR, and CRUD methods remain in `Database`. User values are parameterized, and aggregation is performed in SQLite rather than by loading students and calculating in Python.

## Test checklist

1. Add at least three BCA and two BBA students.
2. Compare `get_total_students()` with the records shown by View All.
3. Manually verify `get_average_marks()` and `get_total_marks()`.
4. Compare highest and lowest values with the source records.
5. Check grouped course counts, averages, highest marks, and lowest marks.
6. Call `get_courses_above_average(80)` and confirm every returned course average is at least 80.
7. Run both statistics menu options with an empty database; they should not crash.

For isolated tests, pass a temporary database path to `Database(db_path)`.

## Assignment answers

1. An aggregate function calculates a value from multiple rows.
2. `COUNT()` counts rows or non-NULL values, depending on its argument.
3. `SUM()` totals numeric values.
4. `AVG()` calculates the mean of non-NULL numeric values.
5. `MIN()` returns the smallest value.
6. `MAX()` returns the largest value.
7. `GROUP BY` collects rows with matching values into groups for aggregate calculations.
8. It enables summaries such as counts or averages per course.
9. `WHERE` filters rows before grouping; `HAVING` filters groups after aggregation.
10. Yes. For example, `WHERE marks >= 60 GROUP BY course` filters rows before calculating each course average.
11. SQLite permits `HAVING` without `GROUP BY`, treating the result as one group, but `HAVING` is most commonly used with grouped aggregate queries.
12. Database-side aggregation avoids transferring every row and lets the database process the calculation efficiently.
13. `AVG()` returns `NULL` for an empty table; this app displays `N/A`.
14. An alias gives a result column a readable name, such as `average_marks`.
15. One combined grouped query returns all course measures together, avoiding repeated scans and keeping the statistics consistent.

## Viva review

- Count students with `SELECT COUNT(*) FROM students`.
- Average marks with `SELECT AVG(marks) FROM students`.
- Highest marks with `SELECT MAX(marks) FROM students`.
- Count by course with `SELECT course, COUNT(*) FROM students GROUP BY course`.
- `WHERE` filters rows; `HAVING` filters aggregate groups.
- Find courses with average marks above 80 using `GROUP BY course HAVING AVG(marks) > 80`.