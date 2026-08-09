-- Members of a group
SELECT u.user_id, u.full_name, u.email
FROM users u
JOIN group_members gm ON gm.user_id = u.user_id
WHERE gm.group_id = $1;

-- Groups joined by a student
SELECT sg.group_id, sg.group_name, sg.course_code
FROM study_groups sg
JOIN group_members gm ON gm.group_id = sg.group_id
WHERE gm.user_id = $1;

-- Student weekly availability
SELECT day_of_week, start_time, end_time
FROM availability
WHERE user_id = $1
ORDER BY day_of_week, start_time;

-- Common group availability
SELECT * FROM find_common_availability($1, 30);

-- Upcoming sessions for a student
SELECT s.session_id, sg.group_name, s.topic, s.session_date, s.start_time, s.end_time
FROM study_sessions s
JOIN study_groups sg ON sg.group_id = s.group_id
JOIN group_members gm ON gm.group_id = sg.group_id
WHERE gm.user_id = $1 AND s.session_date >= CURRENT_DATE
ORDER BY s.session_date, s.start_time;

-- Sessions attended during a semester
SELECT s.session_id, s.topic, s.session_date, a.attendance_status
FROM attendance a
JOIN study_sessions s ON s.session_id = a.session_id
WHERE a.user_id = $1 AND s.session_date BETWEEN $2 AND $3;

-- Attendance percentage
SELECT ROUND(100.0 * SUM(CASE WHEN attendance_status IN ('Present', 'Late') THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS attendance_percentage
FROM attendance
WHERE user_id = $1;

-- Group member count
SELECT COUNT(*) AS member_count
FROM group_members
WHERE group_id = $1;

-- Students without availability
SELECT u.user_id, u.full_name, u.course
FROM users u
LEFT JOIN availability a ON a.user_id = u.user_id
WHERE a.availability_id IS NULL
ORDER BY u.full_name;

-- Group membership report
SELECT sg.course_code, sg.group_name, COUNT(gm.user_id) AS member_count, creator.full_name AS created_by
FROM study_groups sg
LEFT JOIN group_members gm ON gm.group_id = sg.group_id
LEFT JOIN users creator ON creator.user_id = sg.created_by
GROUP BY sg.group_id, sg.course_code, sg.group_name, creator.full_name
ORDER BY sg.course_code, sg.group_name;

-- Attendance summary by group
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
ORDER BY sg.course_code, sg.group_name;

-- Student attendance report
SELECT ss.session_date, sg.group_name, ss.topic, ss.start_time, ss.end_time, a.attendance_status
FROM attendance a
JOIN study_sessions ss ON ss.session_id = a.session_id
JOIN study_groups sg ON sg.group_id = ss.group_id
WHERE a.user_id = $1
ORDER BY ss.session_date DESC, ss.start_time;

-- Upcoming sessions report
SELECT ss.session_date, sg.course_code, sg.group_name, ss.topic, ss.start_time, ss.end_time, ss.location, ss.meeting_link, ss.status
FROM study_sessions ss
JOIN study_groups sg ON sg.group_id = ss.group_id
WHERE ss.session_date >= CURRENT_DATE
ORDER BY ss.session_date, ss.start_time;

-- Most active groups
SELECT sg.course_code, sg.group_name, COUNT(ss.session_id) AS session_count
FROM study_groups sg
LEFT JOIN study_sessions ss ON ss.group_id = sg.group_id AND ss.status IN ('Planned', 'Completed')
GROUP BY sg.group_id, sg.course_code, sg.group_name
ORDER BY session_count DESC, sg.group_name;
