import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db_ops import (
    get_all_remedial_classes, get_performance_by_student, 
    get_attendance_for_student, add_feedback, get_all_subjects
)
from datetime import date
import streamlit_calendar as st_cal

st.set_page_config(page_title="Student Dashboard", layout="wide")

# ----------------- HEADER -----------------
st.title("🎓 Student Dashboard")
user = st.session_state.user
student_id = user["user_id"]

st.markdown(
    f"""
    <div style='background-color:#FFE0E9; padding: 1rem; border-radius: 10px;'>
        <h4 style='color:#444;'>Welcome back, <em>{user['name']}</em>! Here's a quick look at your classes, progress, and attendance.</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------- DATA LOADING -----------------
classes = get_all_remedial_classes()
subjects = {s[0]: s[1] for s in get_all_subjects()}

# ----------------- UPCOMING CLASSES -----------------
with st.container():
    st.subheader("📅 Upcoming Remedial Classes")
    today = date.today()
    upcoming = [c for c in classes if c[3] >= str(today)]

    if upcoming:
        events = []
        for c in upcoming:
            subject = subjects.get(c[1], "Unknown")
            events.append({
                "title": f"{subject} ({c[4]})",
                "start": f"{c[3]}T{c[4]}",
                "end": f"{c[3]}T{c[4]}",
                "location": f"Room {c[5]}"
            })

        st_cal.calendar(events=events, options={"initialView": "dayGridMonth"})
    else:
        st.info("No upcoming classes scheduled.")

# ----------------- PERFORMANCE CHART -----------------
with st.container():
    st.subheader("📈 My Performance")
    perf = get_performance_by_student(student_id)
    if perf:
        perf_df = pd.DataFrame(perf, columns=["ID", "StudentID", "SubjectID", "Before", "After", "Date"])
        perf_df["Subject"] = perf_df["SubjectID"].map(subjects)

        chart = px.line(
            perf_df,
            x="Date",
            y=["Before", "After"],
            color_discrete_map={"Before": "#FFB6B9", "After": "#A3D2CA"},
            labels={"value": "Score", "variable": "Test Type"},
            title="Performance Before vs After Remedial Classes"
        )
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.info("No performance data available.")

# ----------------- ATTENDANCE -----------------
with st.container():
    st.subheader("🗂️ My Attendance Record")
    att = get_attendance_for_student(student_id)
    if att:
        att_df = pd.DataFrame(att, columns=["ID", "ClassID", "StudentID", "Status", "Date"])
        attendance_rate = att_df["Status"].value_counts(normalize=True) * 100
        st.metric("Attendance Rate", f"{attendance_rate.get('present', 0):.1f}% Present")
        st.dataframe(att_df[["Date", "Status"]].sort_values("Date"), use_container_width=True)
    else:
        st.info("No attendance records available.")

# ----------------- FEEDBACK -----------------
with st.container():
    st.subheader("💬 Submit Feedback")
    with st.form("feedback_form"):
        subject = st.selectbox("Subject", list(subjects.values()))
        feedback = st.text_area("Your Feedback", max_chars=500)
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            subject_ids = [k for k, v in subjects.items() if v == subject_name]
            if subject_ids:
                subject_id = subject_ids[0]
                add_feedback(student_id, subject_id, feedback, str(date.today()))
                st.success("Thank you for your feedback!")
            else:
                st.error("Subject not found. Please try again.")

            add_feedback(student_id, subject_id, feedback, str(date.today()))
            st.success("Thank you for your feedback!")
