import streamlit as st
import textwrap
from PIL import Image

from ui import (
    add_spacer,
    current_profile,
    ensure_state,
    icon,
    inject_css,
    is_profile_complete,
    sidebar,
    update_current_profile,
)

app_logo = Image.open("assets/logo.png")

st.set_page_config(
    page_title="Profile | AiDa",
    page_icon=app_logo,
    layout="wide",
)

inject_css()
ensure_state()
sidebar()
profile = current_profile()

st.markdown("## Profile")

if not profile:
    st.info("Start onboarding from the AiDa home page first.")
    st.page_link("app.py", label="Go to AiDa Home")
    st.stop()

status = "Complete" if is_profile_complete(profile) else "In Progress"
st.markdown(
    f"""
<div class="aida-card">
<div class="aida-kicker">{icon("profile", 18)} {status}</div>
<h3>{profile.get("name") or "Your AiDa profile"}</h3>
<div class="aida-label">{profile.get("goal") or "Goal not set yet"}</div>
</div>
""",
    unsafe_allow_html=True,
)

add_spacer("1rem")
st.markdown("### Personal Details")
with st.form("profile_form"):
    col1, col2 = st.columns(2)
    name = col1.text_input("Name", value=profile.get("name") or "")
    age = col2.number_input("Age", min_value=0, max_value=120, value=int(profile.get("age") or 0))
    weight = col1.number_input("Weight (kg)", min_value=0.0, max_value=300.0, value=float(profile.get("weight") or 0), step=0.1)
    height = col2.number_input("Height (cm)", min_value=0.0, max_value=260.0, value=float(profile.get("height") or 0), step=0.5)
    goal = st.text_input("Goal", value=profile.get("goal") or "")
    workout_equipment = st.text_area("Workout Equipment", value=profile.get("workout_equipment") or "")
    workout_preferences = st.text_area("Workout Preferences", value=profile.get("workout_preferences") or "")
    nutrition_preferences = st.text_area("Nutrition Preferences", value=profile.get("nutrition_preferences") or "")
    health_notes = st.text_area("Health Notes", value=profile.get("health_notes") or "")
    aida_notes = st.text_area("AiDa Notes", value=profile.get("aida_notes") or "")
    submitted = st.form_submit_button("Save Profile")

if submitted:
    update_current_profile(
        {
            "name": name,
            "age": age or None,
            "weight": weight or None,
            "height": height or None,
            "goal": goal,
            "workout_equipment": workout_equipment,
            "workout_preferences": workout_preferences,
            "nutrition_preferences": nutrition_preferences,
            "health_notes": health_notes,
            "aida_notes": aida_notes,
        }
    )
    st.success("Profile updated.")
    st.rerun()

add_spacer("1.5rem")
st.markdown("### Memory")
cols = st.columns(3)
cols[0].markdown(
    f"""
    <div class="aida-card">
        <div class="aida-kicker">Training</div>
        <div class="aida-label">{profile.get("workout_preferences") or "No workout preferences yet"}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
cols[1].markdown(
    f"""
    <div class="aida-card">
        <div class="aida-kicker">Nutrition</div>
        <div class="aida-label">{profile.get("nutrition_preferences") or "No nutrition preferences yet"}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
cols[2].markdown(
    f"""
    <div class="aida-card">
        <div class="aida-kicker">Health</div>
        <div class="aida-label">{profile.get("health_notes") or "No health notes yet"}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
