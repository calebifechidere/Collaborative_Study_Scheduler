import logging
from datetime import datetime
import psycopg
from db import execute, execute_with_row, fetch_all, fetch_one


def register_user(full_name, email, course, student_level, password):
    query = """
        INSERT INTO users (full_name, email, course, student_level, password_hash)
        VALUES (%s, %s, %s, %s, crypt(%s, gen_salt('bf')))
        RETURNING user_id
    """
    try:
        row = execute_with_row(query, (full_name, email, course, student_level, password))
        return {"user_id": row[0]} if row else None
    except psycopg.errors.UniqueViolation as exc:
        logging.exception("Registration failed because the email already exists")
        raise ValueError("DUPLICATE_EMAIL") from exc
    except Exception:
        logging.exception("Registration failed")
        raise


def authenticate_user(email, password):
    query = """
        SELECT user_id, full_name, email, course, student_level
        FROM users
        WHERE email = %s AND password_hash = crypt(%s, password_hash)
    """
    return fetch_one(query, (email, password))

DAY_NAMES = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}


def format_day_name(day_value):
    return DAY_NAMES.get(day_value, str(day_value))


def format_time_value(value):
    if value is None:
        return ""
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return ""
        try:
            value = datetime.strptime(text, "%H:%M").time()
        except ValueError:
            return text
    if hasattr(value, "strftime"):
        return value.strftime("%I:%M %p")
    return str(value)


def add_user(full_name, email, course, student_level, password=None):
    password = password or "Study@123"
    query = """
        INSERT INTO users (full_name, email, course, student_level, password_hash)
        VALUES (%s, %s, %s, %s, crypt(%s, gen_salt('bf')))
        RETURNING user_id
    """
    return fetch_one(query, (full_name, email, course, student_level, password))


def create_group(course_code, group_name, created_by):
    query = """
        INSERT INTO study_groups (course_code, group_name, created_by)
        VALUES (%s, %s, %s)
        RETURNING group_id
    """
    return fetch_one(query, (course_code, group_name, created_by))


def join_group(group_id, user_id):
    query = """
        INSERT INTO group_members (group_id, user_id)
        VALUES (%s, %s)
    """
    return execute(query, (group_id, user_id))


def add_availability(user_id, day_of_week, start_time, end_time):
    query = """
        INSERT INTO availability (user_id, day_of_week, start_time, end_time)
        VALUES (%s, %s, %s, %s)
    """
    return execute(query, (user_id, day_of_week, start_time, end_time))


def find_common_availability(group_id, min_minutes=30):
    return fetch_all(
        "SELECT * FROM find_common_availability(%s, %s)",
        (group_id, min_minutes),
    )


def schedule_session(group_id, topic, session_date, start_time, end_time, location, meeting_link, status="Planned"):
    query = """
        INSERT INTO study_sessions (group_id, topic, session_date, start_time, end_time, location, meeting_link, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING session_id
    """
    return fetch_one(query, (group_id, topic, session_date, start_time, end_time, location, meeting_link, status))


def mark_attendance(session_id, user_id, attendance_status):
    query = """
        INSERT INTO attendance (session_id, user_id, attendance_status)
        VALUES (%s, %s, %s)
        ON CONFLICT (session_id, user_id) DO UPDATE
        SET attendance_status = EXCLUDED.attendance_status
    """
    return execute(query, (session_id, user_id, attendance_status))


def dashboard_summary():
    return fetch_one(
        """
        SELECT
            (SELECT COUNT(*) FROM users) AS student_count,
            (SELECT COUNT(*) FROM study_groups) AS group_count,
            (SELECT COUNT(*) FROM study_sessions) AS session_count,
            (SELECT COUNT(*) FROM attendance) AS attendance_count
        """
    )


def get_session_members(session_id):
    query = """
        SELECT gm.user_id, u.full_name
        FROM study_sessions ss
        JOIN study_groups sg ON sg.group_id = ss.group_id
        JOIN group_members gm ON gm.group_id = sg.group_id
        JOIN users u ON u.user_id = gm.user_id
        WHERE ss.session_id = %s
        ORDER BY u.full_name
    """
    return fetch_all(query, (session_id,))


def get_session_attendance(session_id):
    query = """
        SELECT user_id, attendance_status
        FROM attendance
        WHERE session_id = %s
    """
    rows = fetch_all(query, (session_id,))
    return {row["user_id"]: row["attendance_status"] for row in rows}


def save_session_attendance(session_id, updates):
    for user_id, status in updates.items():
        mark_attendance(session_id, user_id, status)
    return True


def get_group_members(group_id):
    query = """
        SELECT
            u.user_id,
            u.full_name,
            u.email,
            u.course,
            u.student_level,
            gm.joined_date,
            CASE
                WHEN sg.created_by = u.user_id THEN 'Creator'
                ELSE 'Member'
            END AS role
        FROM group_members gm
        JOIN users u ON u.user_id = gm.user_id
        JOIN study_groups sg ON sg.group_id = gm.group_id
        WHERE gm.group_id = %s
        ORDER BY
            CASE WHEN sg.created_by = u.user_id THEN 0 ELSE 1 END,
            u.full_name
    """
    return fetch_all(query, (group_id,))


def get_group_membership_report():
    query = """
        SELECT sg.course_code, sg.group_name, COUNT(gm.user_id) AS member_count, creator.full_name AS created_by
        FROM study_groups sg
        LEFT JOIN group_members gm ON gm.group_id = sg.group_id
        LEFT JOIN users creator ON creator.user_id = sg.created_by
        GROUP BY sg.group_id, sg.course_code, sg.group_name, creator.full_name
        ORDER BY sg.course_code, sg.group_name
    """
    return fetch_all(query)


def get_attendance_summary_by_group():
    query = """
        SELECT
            sg.course_code,
            sg.group_name,
            COUNT(DISTINCT ss.session_id) AS total_sessions,
            COUNT(a.session_id) AS total_attendance_records,
            SUM(CASE WHEN a.attendance_status = 'Present' THEN 1 ELSE 0 END) AS present_count,
            SUM(CASE WHEN a.attendance_status = 'Absent' THEN 1 ELSE 0 END) AS absent_count,
            SUM(CASE WHEN a.attendance_status = 'Late' THEN 1 ELSE 0 END) AS late_count,
            SUM(CASE WHEN a.attendance_status = 'Excused' THEN 1 ELSE 0 END) AS excused_count
        FROM study_groups sg
        LEFT JOIN study_sessions ss ON ss.group_id = sg.group_id
        LEFT JOIN attendance a ON a.session_id = ss.session_id
        GROUP BY sg.group_id, sg.course_code, sg.group_name
        ORDER BY sg.course_code, sg.group_name
    """
    return fetch_all(query)


def get_student_attendance_report(user_id):
    query = """
        SELECT ss.session_date, sg.group_name, ss.topic, ss.start_time, ss.end_time, a.attendance_status
        FROM attendance a
        JOIN study_sessions ss ON ss.session_id = a.session_id
        JOIN study_groups sg ON sg.group_id = ss.group_id
        WHERE a.user_id = %s
        ORDER BY ss.session_date DESC, ss.start_time
    """
    return fetch_all(query, (user_id,))


def get_student_attendance_percentage(user_id):
    query = """
        SELECT ROUND(
            100.0 * SUM(CASE WHEN attendance_status IN ('Present', 'Late') THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0),
            2
        ) AS attendance_percentage
        FROM attendance
        WHERE user_id = %s
    """
    row = fetch_one(query, (user_id,))
    return row["attendance_percentage"] if row and row.get("attendance_percentage") is not None else 0


def get_upcoming_sessions_report():
    query = """
        SELECT ss.session_date, sg.course_code, sg.group_name, ss.topic, ss.start_time, ss.end_time, ss.location, ss.meeting_link, ss.status
        FROM study_sessions ss
        JOIN study_groups sg ON sg.group_id = ss.group_id
        WHERE ss.session_date >= CURRENT_DATE
        ORDER BY ss.session_date, ss.start_time
    """
    return fetch_all(query)


def get_students_without_availability():
    query = """
        SELECT u.user_id, u.full_name, u.course
        FROM users u
        LEFT JOIN availability a ON a.user_id = u.user_id
        WHERE a.availability_id IS NULL
        ORDER BY u.full_name
    """
    return fetch_all(query)


def get_most_active_groups():
    query = """
        SELECT sg.course_code, sg.group_name, COUNT(ss.session_id) AS session_count
        FROM study_groups sg
        LEFT JOIN study_sessions ss ON ss.group_id = sg.group_id AND ss.status IN ('Planned', 'Completed')
        GROUP BY sg.group_id, sg.course_code, sg.group_name
        ORDER BY session_count DESC, sg.group_name
    """
    return fetch_all(query)


def compute_common_availability(slots, min_minutes=30):
    if not slots:
        return []

    def to_minutes(value):
        if isinstance(value, str):
            dt = datetime.strptime(value, "%H:%M")
            return dt.hour * 60 + dt.minute
        return value

    normalized = []
    for user_slots in slots:
        intervals = []
        for start, end in user_slots:
            start_min = to_minutes(start)
            end_min = to_minutes(end)
            if end_min > start_min:
                intervals.append((start_min, end_min))
        normalized.append(intervals)

    if not normalized or not normalized[0]:
        return []

    common = normalized[0]
    if len(normalized) == 1:
        return []

    for user_slots in normalized[1:]:
        overlaps = []
        for start_a, end_a in common:
            for start_b, end_b in user_slots:
                overlap_start = max(start_a, start_b)
                overlap_end = min(end_a, end_b)
                if overlap_end - overlap_start >= min_minutes:
                    overlaps.append((overlap_start, overlap_end))
        common = overlaps
        if not common:
            break

    return [
        (f"{start // 60:02d}:{start % 60:02d}", f"{end // 60:02d}:{end % 60:02d}")
        for start, end in common
    ]
