import logging
import streamlit as st
from db import fetch_all
from services import (
    DAY_NAMES,
    add_availability,
    add_user,
    authenticate_user,
    create_group,
    dashboard_summary,
    find_common_availability,
    format_day_name,
    format_time_value,
    get_attendance_summary_by_group,
    get_group_members,
    get_group_membership_report,
    get_most_active_groups,
    get_session_attendance,
    get_session_members,
    get_students_without_availability,
    get_student_attendance_percentage,
    get_student_attendance_report,
    get_upcoming_sessions_report,
    join_group,
    mark_attendance,
    register_user,
    save_session_attendance,
    schedule_session,
)

st.set_page_config(page_title="Collaborative Study Scheduler", page_icon="📚", layout="wide")


def initialize_auth_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if st.session_state.current_user is None and st.session_state.user:
        st.session_state.current_user = st.session_state.user
        st.session_state.authenticated = True
    if st.session_state.current_user is not None and st.session_state.user is None:
        st.session_state.user = st.session_state.current_user


def apply_theme_css():
    st.markdown(
        """
        <style>
        :root { color-scheme: dark; }
        .stApp { background: #0F172A; color: #F8FAFC; }
        [data-testid="stSidebar"] { background-color: #111827; }
        .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
        .stTextInput > div > div > input, .stSelectbox > div > div > div, .stTextArea > div > div > textarea {
            background-color: #0F172A; color: #F8FAFC; border: 1px solid #334155; border-radius: 10px;
        }
        .stButton > button {
            background: linear-gradient(90deg, #14B8A6, #3B82F6); color: white; border: none; border-radius: 10px;
        }
        .auth-card {
            background: #1E293B; border: 1px solid #334155; border-radius: 18px; padding: 1.5rem; box-shadow: 0 10px 35px rgba(2, 6, 23, 0.35);
        }
        .metric-card {
            background: #1E293B; border: 1px solid #334155; border-radius: 14px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
        }
        .metric-title { color: #94A3B8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; }
        .metric-value { color: #F8FAFC; font-size: 1.6rem; font-weight: 700; margin-top: 0.2rem; }
        .metric-icon { color: #14B8A6; font-size: 1.1rem; margin-bottom: 0.25rem; }
        .muted { color: #94A3B8; }
        .accent { color: #14B8A6; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(title, value, icon):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_auth_page():
    apply_theme_css()
    st.title("Collaborative Study Scheduler")
    st.caption("Plan study groups, share weekly availability, and find common meeting times.")

    left_col, right_col = st.columns([1.1, 0.9], gap="large")
    with left_col:
        st.markdown("### Welcome to your academic planning space")
        st.markdown("A calm place to organise study groups, share availability, and find shared meeting windows.")
        st.markdown("")
        st.markdown("- Join course study groups")
        st.markdown("- Share weekly availability")
        st.markdown("- Find common meeting times")
        st.markdown("")

    with right_col:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        tabs = st.tabs(["Login", "Sign Up"])
        with tabs[0]:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                if submit:
                    try:
                        user = authenticate_user(email, password)
                        if user:
                            st.session_state.current_user = user
                            st.session_state.user = user
                            st.session_state.authenticated = True
                            st.success("Welcome back.")
                            st.rerun()
                        else:
                            st.error("Invalid email or password.")
                    except Exception:
                        st.error("Invalid email or password.")
        with tabs[1]:
            with st.form("signup_form"):
                full_name = st.text_input("Full name")

                matric_number = st.text_input(
                    "Matriculation Number",
                    placeholder="e.g. 20241433872",
                    max_chars=11
                )

                email = st.text_input("Email")
                course = st.text_input("Course")

                student_level = st.selectbox(
                    "Student level",
                    [
                        "100",
                        "200",
                        "300",
                        "400",
                        "500",
                        "Undergraduate",
                        "Postgraduate",
                        "Other"
                    ]
                )

                password = st.text_input("Password", type="password")
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password"
                )

                submit = st.form_submit_button("Create account")

                if submit:
                    matric_number = matric_number.strip()

                    if not full_name.strip():
                        st.error("Full name is required.")

                    elif not matric_number:
                        st.error("Matriculation number is required.")

                    elif len(matric_number) != 11 or not matric_number.isdigit():
                        st.error(
                            "Matriculation number must contain exactly 11 digits."
                        )

                    elif not email.strip():
                        st.error("Email is required.")

                    elif not course.strip():
                        st.error("Course is required.")

                    elif student_level not in {
                        "100", "200", "300", "400", "500"
                    }:
                        st.error(
                            "Level must be 100, 200, 300, 400 or 500."
                        )

                    elif len(password) < 8:
                        st.error(
                            "Password must contain at least 8 characters."
                        )

                    elif password != confirm_password:
                        st.error("Passwords do not match.")

                    else:
                        try:
                            user = register_user(
                                full_name.strip(),
                                matric_number,
                                email.strip(),
                                course.strip(),
                                student_level,
                                password
                            )

                            if user:
                                st.session_state.current_user = {
                                    "user_id": user.get("user_id"),
                                    "full_name": full_name.strip(),
                                    "matric_number": matric_number,
                                    "email": email.strip(),
                                    "course": course.strip(),
                                    "student_level": student_level
                                }

                                st.session_state.user = (
                                    st.session_state.current_user
                                )
                                st.session_state.authenticated = True

                                st.success("Registration successful.")
                                st.rerun()

                            else:
                                st.error(
                                    "Unable to create account right now."
                                )

                        except ValueError as exc:
                            if str(exc) == "DUPLICATE_USER":
                                st.error(
                                    "An account with that email or "
                                    "matriculation number already exists."
                                )
                            else:
                                st.error(
                                    "Unable to create account right now."
                                )

                        except Exception:
                            logging.exception("Registration failed")
                            st.error(
                                "Unable to create account right now."
                            )
        st.markdown("</div>", unsafe_allow_html=True)



def render_sidebar():
    with st.sidebar:
        st.markdown("### Navigation")
        user = st.session_state.current_user or {}
        if user:
            st.caption(f"{user.get('full_name', 'Student')}")
            st.caption(f"{user.get('course', '')} • {user.get('student_level', '')}")
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.current_user = None
            st.session_state.user = None
            st.session_state.authenticated = False
            st.rerun()
        st.markdown("---")
        return st.radio("Navigation", ["Dashboard", "Students", "Study Groups", "Availability", "Find Common Time", "Study Sessions", "Attendance", "Reports"], index=0)


initialize_auth_state()
apply_theme_css()

if not st.session_state.authenticated:
    render_auth_page()
    st.stop()

st.title("Collaborative Study Scheduler")
st.caption("Plan study groups, share availability, and find common meeting times.")
page = render_sidebar()


def load_users():
    return fetch_all(
        """
        SELECT
            user_id,
            matric_number,
            full_name,
            email,
            course,
            student_level
        FROM users
        ORDER BY full_name
        """
    )


def load_groups():
    return fetch_all(
        """
        SELECT sg.group_id, sg.group_name, sg.course_code, u.full_name AS created_by, sg.created_at
        FROM study_groups sg
        LEFT JOIN users u ON u.user_id = sg.created_by
        ORDER BY sg.created_at DESC
        """
    )


def load_availability():
    return fetch_all(
        """
        SELECT a.availability_id, u.full_name, a.day_of_week, a.start_time, a.end_time
        FROM availability a
        JOIN users u ON u.user_id = a.user_id
        ORDER BY u.full_name, a.day_of_week, a.start_time
        """
    )


def load_sessions():
    return fetch_all(
        """
        SELECT s.session_id, sg.group_name, s.topic, s.session_date, s.start_time, s.end_time, s.status
        FROM study_sessions s
        JOIN study_groups sg ON sg.group_id = s.group_id
        ORDER BY s.session_date, s.start_time
        """
    )


def load_attendance():
    return fetch_all(
        """
        SELECT a.session_id, u.full_name, a.attendance_status
        FROM attendance a
        JOIN users u ON u.user_id = a.user_id
        ORDER BY a.session_id, u.full_name
        """
    )


def display_table(rows, columns):
    if not rows:
        return
    st.dataframe(rows, column_config={col: {"label": col.replace("_", " ").title()} for col in columns}, use_container_width=True)


def build_user_selector(label, include_all=False):
    users = load_users()
    options = [row["user_id"] for row in users]
    labels = {row["user_id"]: row["full_name"] for row in users}
    if include_all:
        options = [None] + options
        labels[None] = "All students"
    return st.selectbox(label, options, format_func=lambda uid: labels.get(uid, ""))


if page == "Dashboard":
    summary = dashboard_summary()
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_metric_card("Students", summary.get("student_count", 0), "👩‍🎓")
        with col2:
            render_metric_card("Groups", summary.get("group_count", 0), "👥")
        with col3:
            render_metric_card("Sessions", summary.get("session_count", 0), "🗓️")
        with col4:
            render_metric_card("Attendance Records", summary.get("attendance_count", 0), "✅")
    st.subheader("Recent study groups")
    groups = load_groups()
    if groups:
        display_table(groups, ["group_name", "course_code", "created_by"])
    else:
        st.info("No study groups have been created yet.")

elif page == "Students":
    st.subheader("Register a student")
    with st.form("student_form"):
        full_name = st.text_input("Full name")
        email = st.text_input("Email")
        course = st.text_input("Course")
        student_level = st.selectbox("Student level", ["100", "200", "300", "400", "500", "Undergraduate", "Postgraduate", "Other"])
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Save student"):
            try:
                add_user(full_name, email, course, student_level, password or None)
                st.success("Student added successfully.")
            except Exception as exc:
                st.error(f"Could not save the student: {exc}")
    st.subheader("Students")
    users = load_users()
    if users:
        display_table(users, ["full_name", "email", "course", "student_level"])
    else:
        st.info("No students yet. Add the first one above.")

elif page == "Study Groups":
    st.subheader("Create a study group")
    current_user = st.session_state.current_user or {}
    current_user_id = current_user.get("user_id")
    with st.form("group_form"):
        course_code = st.text_input("Course code")
        group_name = st.text_input("Group name")
        if current_user:
            st.text_input("Logged in as", value=current_user.get("full_name", ""), disabled=True)
        if st.form_submit_button("Create group"):
            try:
                if not current_user_id:
                    st.error("You must be logged in to create a group.")
                else:
                    create_group(course_code, group_name, current_user_id)
                    st.success("Group created successfully.")
            except Exception as exc:
                st.error(f"Could not create the group: {exc}")
    st.subheader("Join a group")
    with st.form("join_group_form"):
        groups = load_groups()
        group_id = st.selectbox("Group", [row["group_id"] for row in groups], format_func=lambda gid: next(g["course_code"] + " — " + g["group_name"] for g in groups if g["group_id"] == gid))
        if current_user:
            st.text_input("Logged in as", value=current_user.get("full_name", ""), disabled=True)
        if st.form_submit_button("Join group"):
            try:
                if not current_user_id:
                    st.error("You must be logged in to join a group.")
                else:
                    join_group(group_id, current_user_id)
                    st.success("You joined the group.")
            except Exception as exc:
                st.error(f"Could not add membership: {exc}")
    st.subheader("Study groups")
    groups = load_groups()
    if groups:
        display_table(groups, ["group_name", "course_code", "created_by"])
    else:
        st.info("No groups have been created yet.")

    st.subheader("View Group Members")
    groups = load_groups()
    if groups:
        selected_group_id = st.selectbox("Select group", [row["group_id"] for row in groups], format_func=lambda gid: next(g["course_code"] + " — " + g["group_name"] for g in groups if g["group_id"] == gid), key="member_group")
        selected_group = next((g for g in groups if g["group_id"] == selected_group_id), None)
        members = get_group_members(selected_group_id)
        if selected_group:
            st.caption(f"Group name: {selected_group['group_name']}")
            st.caption(f"Course code: {selected_group['course_code']}")
            if members:
                creator_name = next((row["full_name"] for row in members if row.get("role") == "Creator"), "")
                st.caption(f"Total members: {len(members)}")
                st.caption(f"Group creator: {creator_name or 'Unknown'}")
                member_rows = []
                for row in members:
                    member_rows.append({
                        "Full Name": row.get("full_name"),
                        "Email": row.get("email"),
                        "Course": row.get("course"),
                        "Level": row.get("student_level"),
                        "Role": row.get("role"),
                        "Joined Date": row.get("joined_date"),
                    })
                st.dataframe(member_rows, use_container_width=True)
            else:
                st.info("This group currently has no members.")
        else:
            st.info("Select a group to view members.")
    else:
        st.info("Create a group first to view members.")

elif page == "Availability":
    st.subheader("Add recurring availability")
    with st.form("availability_form"):
        student = st.selectbox("Student", [row["user_id"] for row in load_users()], format_func=lambda uid: next(u["full_name"] for u in load_users() if u["user_id"] == uid))
        day_value = st.selectbox("Day", list(DAY_NAMES.keys()), format_func=lambda day: DAY_NAMES[day])
        start_time = st.text_input("Start time", value="16:00")
        end_time = st.text_input("End time", value="18:00")
        if st.form_submit_button("Save slot"):
            try:
                add_availability(student, day_value, start_time, end_time)
                st.success("Availability saved.")
            except Exception as exc:
                st.error(f"Could not save availability: {exc}")
    st.subheader("Weekly availability")
    availability = load_availability()
    if availability:
        formatted = []
        for row in availability:
            formatted.append({
                "Student": row["full_name"],
                "Day": format_day_name(row["day_of_week"]),
                "Start Time": format_time_value(row["start_time"]),
                "End Time": format_time_value(row["end_time"]),
            })
        st.dataframe(formatted, use_container_width=True)
    else:
        st.info("No availability has been added yet.")

elif page == "Find Common Time":
    st.subheader("Find common availability")
    groups = load_groups()
    if groups:
        group_id = st.selectbox("Select group", [row["group_id"] for row in groups], format_func=lambda gid: next(g["group_name"] for g in groups if g["group_id"] == gid))
        min_minutes = st.slider("Minimum duration (minutes)", 15, 180, 30, 15)
        if st.button("Find overlap"):
            try:
                results = find_common_availability(group_id, min_minutes)
                if results:
                    formatted = []
                    for row in results:
                        formatted.append({
                            "Day": format_day_name(row.get("day_of_week")),
                            "Common Start Time": format_time_value(row.get("common_start_time")),
                            "Common End Time": format_time_value(row.get("common_end_time")),
                            "Duration (Minutes)": row.get("duration_minutes"),
                        })
                    st.dataframe(formatted, use_container_width=True)
                else:
                    st.info("This group currently has no common availability.")
            except Exception as exc:
                st.error(f"Could not compute overlap: {exc}")
    else:
        st.info("Create a group first to find common time.")

elif page == "Study Sessions":
    st.subheader("Schedule a study session")
    with st.form("session_form"):
        group_id = st.selectbox("Group", [row["group_id"] for row in load_groups()], format_func=lambda gid: next(g["group_name"] for g in load_groups() if g["group_id"] == gid))
        topic = st.text_input("Topic")
        session_date = st.date_input("Date")
        start_time = st.text_input("Start time", value="18:00")
        end_time = st.text_input("End time", value="20:00")
        location = st.text_input("Location", value="Library")
        meeting_link = st.text_input("Meeting link", value="")
        if st.form_submit_button("Schedule session"):
            try:
                schedule_session(group_id, topic, str(session_date), start_time, end_time, location, meeting_link)
                st.success("Session scheduled.")
            except Exception as exc:
                st.error(f"Could not schedule the session: {exc}")
    st.subheader("Upcoming sessions")
    sessions = load_sessions()
    if sessions:
        formatted = []
        for row in sessions:
            formatted.append({
                "Group": row["group_name"],
                "Topic": row["topic"],
                "Date": row["session_date"],
                "Start Time": format_time_value(row["start_time"]),
                "End Time": format_time_value(row["end_time"]),
                "Status": row["status"],
            })
        st.dataframe(formatted, use_container_width=True)
    else:
        st.info("No sessions have been scheduled yet.")

elif page == "Attendance":
    st.subheader("Mark attendance")
    session_options = load_sessions()
    session_id = st.selectbox("Session", [row["session_id"] for row in session_options], format_func=lambda sid: next(s["topic"] for s in session_options if s["session_id"] == sid))
    if session_id:
        try:
            members = get_session_members(session_id)
            existing = get_session_attendance(session_id)
            if members:
                st.caption("Select a status for each group member.")
                entries = {}
                for member in members:
                    user_id = member["user_id"]
                    status = st.selectbox(
                        f"{member['full_name']}",
                        ["Present", "Absent", "Late", "Excused"],
                        index=["Present", "Absent", "Late", "Excused"].index(existing.get(user_id, "Absent")),
                        key=f"status_{user_id}",
                    )
                    entries[user_id] = status
                if st.button("Save attendance"):
                    try:
                        save_session_attendance(session_id, entries)
                        st.success("Attendance saved successfully.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not save attendance: {exc}")
                existing = get_session_attendance(session_id)
                summary = {"Total Members": len(members)}
                summary["Present"] = sum(1 for member in members if existing.get(member["user_id"], "Absent") == "Present")
                summary["Absent"] = sum(1 for member in members if existing.get(member["user_id"], "Absent") == "Absent")
                summary["Late"] = sum(1 for member in members if existing.get(member["user_id"], "Absent") == "Late")
                summary["Excused"] = sum(1 for member in members if existing.get(member["user_id"], "Absent") == "Excused")
                total = len(members)
                summary["Attendance Percentage"] = round(((summary["Present"] + summary["Late"]) / total * 100) if total else 0, 2) if total else 0
                st.subheader("Attendance summary")
                st.write(summary)
                attendance = load_attendance()
                if attendance:
                    st.dataframe(attendance, use_container_width=True)
                else:
                    st.info("No attendance has been recorded for this session.")
            else:
                st.info("No group members are linked to this session.")
        except Exception as exc:
            st.error(f"Could not load attendance form: {exc}")

else:
    st.subheader("Reports")
    st.info("Use these sections to review participation and common meeting times.")
    summary = dashboard_summary()
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_metric_card("Total Students", summary.get("student_count", 0), "👩‍🎓")
        with col2:
            render_metric_card("Total Study Groups", summary.get("group_count", 0), "👥")
        with col3:
            render_metric_card("Total Study Sessions", summary.get("session_count", 0), "🗓️")
        with col4:
            render_metric_card("Total Attendance Records", summary.get("attendance_count", 0), "✅")
    tabs = st.tabs(["Group Membership", "Attendance by Group", "Student Attendance", "Upcoming Sessions", "Students Without Availability", "Most Active Groups", "Common Availability"])
    with tabs[0]:
        rows = get_group_membership_report()
        if rows:
            display_table(rows, ["course_code", "group_name", "member_count", "created_by"])
        else:
            st.info("No group membership data is available.")
    with tabs[1]:
        rows = get_attendance_summary_by_group()
        if rows:
            display_table(rows, ["course_code", "group_name", "total_sessions", "total_attendance_records", "present_count", "absent_count", "late_count", "excused_count"])
        else:
            st.info("No attendance summary is available.")
    with tabs[2]:
        student_id = st.selectbox("Select student", [row["user_id"] for row in load_users()], format_func=lambda uid: next(u["full_name"] for u in load_users() if u["user_id"] == uid))
        rows = get_student_attendance_report(student_id)
        if rows:
            formatted_rows = []
            for row in rows:
                formatted_rows.append({
                    "Session Date": row.get("session_date"),
                    "Group": row.get("group_name"),
                    "Topic": row.get("topic"),
                    "Start Time": format_time_value(row.get("start_time")),
                    "End Time": format_time_value(row.get("end_time")),
                    "Attendance Status": row.get("attendance_status"),
                })
            st.dataframe(formatted_rows, use_container_width=True)
            pct = get_student_attendance_percentage(student_id)
            st.metric("Overall Attendance Percentage", f"{pct:.2f}%")
        else:
            st.info("No attendance history found for this student.")
    with tabs[3]:
        rows = get_upcoming_sessions_report()
        if rows:
            formatted_rows = []
            for row in rows:
                formatted_rows.append({
                    "Session Date": row.get("session_date"),
                    "Course Code": row.get("course_code"),
                    "Group Name": row.get("group_name"),
                    "Topic": row.get("topic"),
                    "Start Time": format_time_value(row.get("start_time")),
                    "End Time": format_time_value(row.get("end_time")),
                    "Location": row.get("location") or row.get("meeting_link"),
                    "Status": row.get("status"),
                })
            st.dataframe(formatted_rows, use_container_width=True)
        else:
            st.info("No upcoming sessions were found.")
    with tabs[4]:
        rows = get_students_without_availability()
        if rows:
            display_table(rows, ["full_name", "course"])
        else:
            st.info("All students have entered availability.")
    with tabs[5]:
        rows = get_most_active_groups()
        if rows:
            display_table(rows, ["course_code", "group_name", "session_count"])
        else:
            st.info("No groups have been scheduled yet.")
    with tabs[6]:
        groups = load_groups()
        if groups:
            group_id = st.selectbox("Select group", [row["group_id"] for row in groups], format_func=lambda gid: next(g["group_name"] for g in groups if g["group_id"] == gid), key="report_group")
            min_minutes = st.slider("Minimum duration (minutes)", 15, 180, 30, 15, key="report_minutes")
            results = find_common_availability(group_id, min_minutes)
            if results:
                formatted_rows = []
                for row in results:
                    formatted_rows.append({
                        "Weekday": format_day_name(row.get("day_of_week")),
                        "Common Start Time": format_time_value(row.get("common_start_time")),
                        "Common End Time": format_time_value(row.get("common_end_time")),
                        "Duration (Minutes)": row.get("duration_minutes"),
                    })
                st.dataframe(formatted_rows, use_container_width=True)
            else:
                st.info("This group currently has no common availability.")
        else:
            st.info("Create a group first to view common availability.")
