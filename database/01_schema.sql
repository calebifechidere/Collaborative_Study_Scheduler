DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS study_sessions;
DROP TABLE IF EXISTS availability;
DROP TABLE IF EXISTS group_members;
DROP TABLE IF EXISTS study_groups;
DROP TABLE IF EXISTS users;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    course VARCHAR(100) NOT NULL,
    student_level VARCHAR(30) NOT NULL CHECK (student_level IN ('100', '200', '300', '400', '500', 'Undergraduate', 'Postgraduate', 'Other')),
    password_hash TEXT NOT NULL
);

CREATE TABLE study_groups (
    group_id SERIAL PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL,
    group_name VARCHAR(100) NOT NULL,
    created_by INTEGER NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE group_members (
    group_id INTEGER NOT NULL REFERENCES study_groups(group_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE availability (
    availability_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    CHECK (start_time < end_time)
);

CREATE TABLE study_sessions (
    session_id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES study_groups(group_id) ON DELETE CASCADE,
    topic VARCHAR(150) NOT NULL,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    location VARCHAR(100) NOT NULL,
    meeting_link VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'Planned' CHECK (status IN ('Planned', 'Completed', 'Cancelled')),
    CHECK (start_time < end_time)
);

CREATE TABLE attendance (
    session_id INTEGER NOT NULL REFERENCES study_sessions(session_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    attendance_status VARCHAR(20) NOT NULL CHECK (attendance_status IN ('Present', 'Absent', 'Late', 'Excused')),
    PRIMARY KEY (session_id, user_id)
);
