# Collaborative Study Scheduler

## Project overview
This project is a beginner-friendly PostgreSQL and Streamlit application for managing study groups, weekly availability, study sessions, and attendance.

## Features
- Register students and sign in securely
- Create and join course-based study groups
- Add recurring weekly availability
- Find common availability windows for a group
- Schedule study sessions
- Record attendance
- Review simple reports

## Technology used
- PostgreSQL
- Python
- psycopg 3
- Streamlit
- python-dotenv
- pytest
- Docker Compose

## Folder structure
- database/: SQL schema, seed data, overlap function, and report queries
- docs/: project report and defence notes
- tests/: pytest tests

## Database tables
- users
- study_groups
- group_members
- availability
- study_sessions
- attendance

## ER diagram
The ER diagram is stored in database/erd.dbml.

## Sample students
The sample students below are fictional demonstration names and emails created for this project.

- Daniel Okafor
- Grace Nwosu
- Michael Eze
- Jessica Umeh
- Samuel Okeke
- Amara Chukwu
- David Brown
- Emily Carter
- Chinedu Nnamani
- Ngozi Ihejirika
- James Wilson
- Sophia Bennett

## Sample groups
The sample groups below are fictional demonstration groups using FUTO-style course codes for presentation purposes.

- COS 201 — Data Structures Study Group
- CYB 201 — Cybersecurity Fundamentals Group
- CYB 203 — Network Security Study Group
- CYB 205 — Digital Forensics Study Group

## Setup instructions for Kali Linux
```bash
cp .env.example .env
docker compose up -d
psql -h localhost -U scheduler_user -d study_scheduler -f database/01_schema.sql
psql -h localhost -U scheduler_user -d study_scheduler -f database/02_seed_data.sql
psql -h localhost -U scheduler_user -d study_scheduler -f database/03_overlap_function.sql
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## PostgreSQL and pgAdmin commands
```bash
# PostgreSQL shell
psql -h localhost -U scheduler_user -d study_scheduler

# Stop containers
docker compose down
```

## Streamlit start command
```bash
streamlit run app.py
```

## Test command
```bash
pytest -q
```

## Demonstration procedure
1. Start PostgreSQL and pgAdmin.
2. Load the SQL files.
3. Open the Streamlit app.
4. Login with a seeded demo account such as daniel.okafor@student.example.com and password Study@123.
5. Create a group and add members.
6. Add availability.
7. Find common time.
8. Schedule a session and mark attendance.

## Screenshots checklist
- Dashboard metrics
- Student form and table
- Group creation and membership
- Availability input
- Common time result
- Session scheduling
- Attendance marking
