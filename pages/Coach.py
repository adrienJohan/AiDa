import streamlit as st
import textwrap
from PIL import Image

from agents.orchestrator import process_message
from agents.response_agent import humanize_response
from ui import (
    add_spacer,
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

app_logo = Image.open("assets/logo.png")

st.set_page_config(
    page_title="Coach | AiDa",
    page_icon=app_logo,
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


# ── Camera dialog (clean modal pop-up) ──────────────────────────────
@st.dialog("Take a Photo")
def camera_dialog():
    """Opens a clean modal with the device camera."""
    camera = st.camera_input("Capture your meal")
    if camera is not None and st.button("Use this photo", type="primary"):
        path = save_upload(camera)
        st.session_state.pending_photo_log = False
        ask_aida("Analyze this meal photo.", mode="nutrition", image_path=path)
        st.rerun()


# ── Conversation ────────────────────────────────────────────────────
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


# ── Inline photo input (appears at the bottom of chat) ──────────────
if st.session_state.get("pending_photo_log"):
    st.markdown(
        f"""
<div class="aida-message-ai">
<div class="aida-message-name">AiDa</div>
<div>Upload a photo of your meal or take one with your camera.</div>
</div>
""",
        unsafe_allow_html=True,
    )
    
    with st.container(border=True):
        uploaded = st.file_uploader(
            "Upload a meal photo",
            type=["jpg", "jpeg", "png"],
            key="coach_photo_upload",
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Take Photo", use_container_width=True):
                camera_dialog()
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.pending_photo_log = False
                st.rerun()
        with col3:
            analyze_disabled = uploaded is None
            if st.button("Analyze", type="primary", use_container_width=True, disabled=analyze_disabled):
                path = save_upload(uploaded)
                st.session_state.pending_photo_log = False
                ask_aida("Analyze this meal photo.", mode="nutrition", image_path=path)
                st.rerun()


# ── Quick-action chips ──────────────────────────────────────────────
st.markdown('<div class="quick-chips-container"></div>', unsafe_allow_html=True)
cols = st.columns(4)
if cols[0].button("Completed Workout", use_container_width=True):
    ask_aida("I completed today's workout.", mode="coach")
    st.rerun()
if cols[1].button("Log Meal", use_container_width=True):
    prompt_message = humanize_response("The user clicked a button to log a meal. Ask them to describe what they ate in the chat.")
    st.session_state.aida_messages.append({"role": "assistant", "content": prompt_message})
    st.rerun()
if cols[2].button("Analyze Meal Photo", use_container_width=True):
    st.session_state.pending_photo_log = True
    st.rerun()
if cols[3].button("Weekly Report", use_container_width=True):
    ask_aida("Give me my weekly report.", mode="weekly_report")
    st.rerun()
