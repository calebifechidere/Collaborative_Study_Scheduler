# Defence Notes

## Simple explanation of every part
- users stores student information.
- study_groups stores each study group.
- group_members links students to groups.
- availability stores weekly availability slots.
- study_sessions stores scheduled meetings.
- attendance records whether each student attended.

## Five-minute demonstration script
1. Show the dashboard metrics.
2. Highlight the fictional sample students such as Daniel Okafor and Grace Nwosu.
3. Log in with the demo account daniel.okafor@student.example.com and password Study@123 to show the secure entry screen.
4. Open one sample group such as COS 201 and explain the study-group setup.
5. Show the availability records and demonstrate the common-time result for Monday evening.
6. Open a sample session topic such as Arrays, Linked Lists and Time Complexity and mark attendance.
7. Explain that the names, emails and course codes are fictional demonstration data.

## Likely defence questions and answers
1. Why PostgreSQL? Because it handles relationships well and supports strict constraints.
2. What is a primary key? A unique identifier for a row.
3. What is a foreign key? A link to another table.
4. Why use composite keys? They prevent duplicate membership or attendance rows.
5. What is the difference between availability and sessions? Availability is weekly recurring free time, while sessions are actual meetings.
6. How does the overlap algorithm work? It compares all members' availability and returns overlapping intervals.
7. What happens if a student has no availability? They will not appear in common-time results.
8. What is the purpose of attendance? It tracks participation.
9. Why are the sample names fictional? They are simple demonstration examples and do not represent real students.
10. Why are the course codes written as COS 201 and CYB 201? They are sample course-style labels for the project demonstration.

## Most important SQL query
The overlap function is the most important query because it finds the shared time periods for all members of a group.

## Reasons for choosing PostgreSQL
PostgreSQL is reliable, supports SQL constraints and is a strong fit for this relational project.

## Limitations and future improvements
The app currently uses simple forms and local deployment. Future work could add authentication, richer reports, and a more advanced scheduler.
