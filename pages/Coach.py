import streamlit as st

from agents.orchestrator import process_message
from ui import (
    ask_aida,
    current_profile,
    ensure_state,
    icon,
    inject_css,
    render_messages,
    save_upload,
    seed_recent_messages,
    sidebar,
)


st.set_page_config(
    page_title="Coach | AiDa",
    page_icon="assets/logo.png",
    layout="wide",
)

inject_css()
ensure_state()
sidebar()
profile = current_profile()
seed_recent_messages()

st.markdown("## Coach")

if not profile:
    st.info("Start onboarding from the AiDa home page first.")
    st.page_link("app.py", label="Go to AiDa Home")
    st.stop()

st.markdown(
    f"""
    <div class="aida-card">
        <div class="aida-kicker">{icon("logo", 18)} AiDa</div>
        <h3>Welcome back {profile.get("name") or ""}</h3>
        <div class="aida-label">What would you like to work on today?</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Quick Actions")
cols = st.columns(5)
if cols[0].button("Completed Workout", use_container_width=True):
    ask_aida("I completed today's workout.", mode="coach")
    st.rerun()
if cols[1].button("Log Meal", use_container_width=True):
    st.session_state.pending_meal_log = True
if cols[2].button("Analyze Meal Photo", use_container_width=True):
    st.session_state.pending_photo_log = True
if cols[3].button("Update Weight", use_container_width=True):
    st.session_state.pending_weight_update = True
if cols[4].button("Weekly Report", use_container_width=True):
    ask_aida("Give me my weekly report.", mode="weekly_report")
    st.rerun()

if st.session_state.get("pending_meal_log"):
    with st.form("meal_log_form", clear_on_submit=True):
        meal = st.text_area("Meal", placeholder="For lunch I ate chicken, rice, and vegetables.")
        submitted = st.form_submit_button("Log Meal")
    if submitted and meal.strip():
        st.session_state.pending_meal_log = False
        ask_aida(meal, mode="nutrition")
        st.rerun()

if st.session_state.get("pending_weight_update"):
    with st.form("weight_update_form", clear_on_submit=True):
        weight = st.number_input("Current weight", min_value=20.0, max_value=300.0, step=0.1)
        submitted = st.form_submit_button("Save Weight")
    if submitted:
        st.session_state.pending_weight_update = False
        ask_aida(f"I weigh {weight} kg now.", mode="weight_update")
        st.rerun()

if st.session_state.get("pending_photo_log"):
    uploaded = st.file_uploader("Meal photo", type=["jpg", "jpeg", "png"])
    camera = st.camera_input("Take a meal photo")
    image = uploaded or camera
    if image is not None and st.button("Analyze Photo", type="primary"):
        path = save_upload(image)
        st.session_state.pending_photo_log = False
        ask_aida("Analyze this meal photo.", mode="nutrition", image_path=path)
        st.rerun()

st.markdown("### Conversation")
if not st.session_state.aida_messages:
    st.session_state.aida_messages.append(
        {
            "role": "assistant",
            "content": "I can help you create a workout plan, log meals, analyze progress, update weight, or generate a weekly report.",
        }
    )

message = st.chat_input("Talk to AiDa")
if message:
    st.session_state.aida_messages.append({"role": "user", "content": message})
    render_messages(st.session_state.aida_messages[-14:])
    try:
        with st.spinner("AiDa is thinking..."):
            response = process_message(message, st.session_state.aida_session)
    except Exception as exc:
        response = (
            "I couldn't complete that request right now. "
            "Check your Gemini API configuration and try again.\n\n"
            f"Technical detail: {exc}"
        )
    st.session_state.aida_messages.append({"role": "assistant", "content": response})
    st.rerun()

render_messages(st.session_state.aida_messages[-14:])
