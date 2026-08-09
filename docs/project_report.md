# Project Report

## Introduction
This project helps students coordinate study groups with PostgreSQL and Streamlit.

## Problem statement
Students often struggle to find shared time slots and organize group study sessions.

## Objectives
- Store student information
- Organize study groups
- Record weekly availability
- Find common time periods
- Manage study sessions and attendance

## Database design
The database uses six main tables to link students, groups, availability, sessions and attendance. The sample data uses fictional Nigerian-style names, emails, and FUTO-style course codes for demonstration only.

## Implementation
The application uses PostgreSQL for storage and Streamlit for the user interface. The overlap logic is implemented in the SQL function in database/03_overlap_function.sql. Sample data includes groups such as COS 201 and CYB 201, with realistic study-session topics such as arrays, cybersecurity threats, network attacks, digital evidence, and database revision.

## Overlap algorithm
The overlap function checks every member's availability and finds periods where all members are available for a given day. The seeded data is arranged so that COS 201 has a common Monday window from 5:00 PM to 6:00 PM, CYB 201 has multiple shared intervals, CYB 203 has no full-group overlap, and CYB 205 has at least one valid shared slot.

## Testing
The test suite covers basic overlap cases and minimum-duration filtering.

## Results
The project provides a simple yet complete study scheduler for beginner-level demonstration with realistic sample data.

## Conclusion
The application demonstrates how relational databases can support collaborative planning in a simple academic setting.
