import streamlit as st
import textwrap
from PIL import Image

from ui import (
    add_spacer,
    ask_aida,
    current_profile,
    ensure_state,
    icon,
    inject_css,
    mark_completed,
    metric_data,
    sidebar,
    workouts_dataframe,
)

app_logo = Image.open("assets/logo.png")

st.set_page_config(
    page_title="Workout | AiDa",
    page_icon=app_logo,
    layout="wide",
)

inject_css()
ensure_state()
sidebar()
profile = current_profile()

st.markdown("## Workout")

if not profile:
    st.info("Start onboarding from the AiDa home page first.")
    st.page_link("app.py", label="Go to AiDa Home")
    st.stop()

metrics = metric_data(profile["id"])
workouts = metrics["workouts"]

top = st.columns(4)
top[0].metric("Planned Sessions", metrics["total"])
top[1].metric("Completed", metrics["completed"])
top[2].metric("Completion Rate", f"{metrics['completion_rate']}%")
top[3].metric("Goal", profile.get("goal") or "Not set")

if not workouts:
    st.markdown(
        f"""
<div class="aida-card">
<div class="aida-kicker">{icon("dumbbell", 18)} Workout Plan</div>
<h3>No plan yet</h3>
<div class="aida-label">Generate a weekly plan with AiDa, then it will appear here as completion cards.</div>
</div>
""",
        unsafe_allow_html=True,
    )
    if st.button("Create Workout Plan", type="primary"):
        ask_aida("Create a workout plan for me.", mode="coach")
        st.rerun()
    st.stop()

add_spacer("1rem")
st.markdown("### Workout Plan")
for row in workouts:
    status = row[6]
    status_text = "Completed" if status == "completed" else "Planned"
    with st.container():
        st.markdown(
            f"""
<div class="aida-card aida-session {status}">
<div class="aida-kicker">{row[3]} · {status_text}</div>
<h3>{row[4]}</h3>
<div class="aida-label">{row[5]}</div>
</div>
""",
            unsafe_allow_html=True,
        )
        if status != "completed":
            if st.button("Mark Complete", key=f"complete_{row[0]}"):
                mark_completed(profile["id"], row[3])
                st.rerun()

add_spacer("1rem")
st.markdown("### Workout History")
df = workouts_dataframe(workouts)
st.dataframe(
    df[["week_start", "day", "workout_name", "status"]],
    use_container_width=True,
    hide_index=True,
)
