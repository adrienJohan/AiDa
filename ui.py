import base64
import os
import sqlite3
import tempfile
from datetime import date

import pandas as pd
import streamlit as st
import textwrap

from agents.orchestrator import process_message
from core.session import create_session, set_mode
from database.db import init_db
from memory.memory import (
    get_meals,
    get_profile,
    get_recent_conversations,
    get_weight_logs,
    get_workout_sessions,
    mark_workout_session_completed,
    update_profile,
)
from markdown_it import MarkdownIt

md = MarkdownIt()


DB_PATH = "data/aida.db"


def inject_css():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
--aida-forest: #1B4332;
--aida-green: #2D6A4F;
--aida-success: #40916C;
--aida-warning: #D4A373;
--aida-bg: #F8F9F6;
--aida-card: #FFFFFF;
--aida-text: #1A1A1A;
--aida-muted: #66736D;
--aida-line: #E2E8E1;
}

html, body, [class*="css"] {
font-family: Inter, sans-serif;
}

.stApp {
background: var(--aida-bg);
color: var(--aida-text);
}

h1, h2, h3 {
color: var(--aida-forest);
letter-spacing: 0;
}

div[data-testid="stSidebarContent"] {
background: #ffffff;
border-right: 1px solid var(--aida-line);
}

.aida-hero {
min-height: 58vh;
display: flex;
align-items: center;
padding: 28px 0 18px;
}

.aida-hero h1 {
font-size: clamp(38px, 7vw, 64px);
line-height: 1;
margin: 0 0 16px;
max-width: 760px;
}

.aida-copy {
color: var(--aida-muted);
font-size: 18px;
line-height: 1.65;
max-width: 700px;
}

.aida-metric {
font-size: 30px;
font-weight: 800;
color: var(--aida-forest);
line-height: 1.1;
}

.aida-card {
background: var(--aida-card);
border: 1px solid var(--aida-line);
border-radius: 8px;
padding: 24px;
box-shadow: 0 8px 24px rgba(27, 67, 50, 0.06);
height: 100%;
margin-bottom: 20px;
}

.aida-card h3 {
font-size: 19px;
margin: 0 0 12px;
}

.aida-label {
color: var(--aida-muted);
font-size: 14px;
margin-top: 5px;
}

.aida-pill {
display: inline-flex;
align-items: center;
gap: 8px;
padding: 6px 10px;
border-radius: 999px;
background: #EDF6F1;
color: var(--aida-forest);
font-size: 13px;
font-weight: 700;
margin: 2px 6px 2px 0;
}

.aida-session {
border-left: 4px solid var(--aida-green);
}

.aida-session.completed {
border-left-color: var(--aida-success);
background: #F1FAF5;
}

.aida-session.planned {
border-left-color: var(--aida-warning);
}

.aida-message-user,
.aida-message-ai {
border-radius: 8px;
padding: 14px 16px;
margin: 10px 0;
border: 1px solid var(--aida-line);
}

.aida-message-user {
background: #F1F4EF;
}

.aida-message-ai {
background: #FFFFFF;
border-left: 4px solid var(--aida-green);
}

.aida-message-name {
font-size: 12px;
font-weight: 800;
color: var(--aida-green);
text-transform: uppercase;
letter-spacing: .08em;
margin-bottom: 6px;
}

.stButton, .stDownloadButton {
margin-top: 10px;
margin-bottom: 10px;
}

.stButton > button,
.stDownloadButton > button {
border-radius: 8px;
border: 1px solid var(--aida-green);
color: var(--aida-forest);
font-weight: 700;
padding: 0.5rem 1rem;
}

.stButton > button[kind="primary"] {
background: var(--aida-forest);
border-color: var(--aida-forest);
color: #FFFFFF;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
border-color: var(--aida-forest);
color: var(--aida-forest);
background: #EDF6F1;
}

.stButton > button[kind="primary"]:hover {
background: var(--aida-green);
border-color: var(--aida-green);
color: #FFFFFF;
}

div[data-testid="stMetricValue"] {
color: var(--aida-forest);
}

.aida-message-user p, .aida-message-ai p {
margin: 0 0 8px 0;
}
.aida-message-user p:last-child, .aida-message-ai p:last-child {
margin-bottom: 0;
}
.aida-message-user h1, .aida-message-ai h1,
.aida-message-user h2, .aida-message-ai h2,
.aida-message-user h3, .aida-message-ai h3 {
margin: 12px 0 6px 0;
color: var(--aida-forest);
font-weight: 700;
line-height: 1.2;
}
.aida-message-user h1, .aida-message-ai h1 { font-size: 1.3em; }
.aida-message-user h2, .aida-message-ai h2 { font-size: 1.2em; }
.aida-message-user h3, .aida-message-ai h3 { font-size: 1.1em; }
.aida-message-user ul, .aida-message-ai ul,
.aida-message-user ol, .aida-message-ai ol {
margin: 8px 0 8px 24px;
padding: 0;
}
.aida-message-user li, .aida-message-ai li {
margin-bottom: 4px;
}
.aida-message-user strong, .aida-message-ai strong {
color: var(--aida-forest);
font-weight: 700;
}

.aida-message-img {
max-width: 320px;
border-radius: 8px;
margin: 10px 0 4px;
border: 1px solid var(--aida-line);
}

.aida-label p {
margin: 0 0 4px 0;
}
.aida-label p:last-child {
margin-bottom: 0;
}
.aida-label ul, .aida-label ol {
margin: 4px 0 4px 20px;
padding: 0;
}

/* Spacing utilities */
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }

</style>
""",
        unsafe_allow_html=True,
    )


def add_spacer(height="1rem"):
    st.markdown(f'<div style="margin-top: {height};"></div>', unsafe_allow_html=True)


def icon(name, size=22):
    paths = {
        "logo": '<path d="M12 3 4 7v6c0 5 3.4 8.1 8 10 4.6-1.9 8-5 8-10V7l-8-4Z"/><path d="M8.5 13.5 11 16l5-6"/>',
        "dumbbell": '<path d="M6 7v10M18 7v10M3 10v4M21 10v4M6 12h12"/>',
        "meal": '<path d="M7 3v18M4 3v6a3 3 0 0 0 6 0V3M16 3v18M16 3c3 2 4 5 2 9h-2"/>',
        "progress": '<path d="M4 19V5M4 19h16M8 16v-5M13 16V8M18 16v-8"/>',
        "profile": '<path d="M20 21a8 8 0 0 0-16 0"/><circle cx="12" cy="7" r="4"/>',
        "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3"/>',
        "check": '<path d="M20 6 9 17l-5-5"/>',
    }
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        f'{paths.get(name, paths["logo"])}</svg>'
    )


def db_rows(query, params=()):
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = [dict(row) for row in conn.execute(query, params).fetchall()]
    conn.close()
    return rows


def latest_profile_id():
    rows = db_rows("SELECT id FROM profiles ORDER BY id DESC LIMIT 1")
    return rows[0]["id"] if rows else None


def is_profile_complete(profile):
    if not profile:
        return False
    return all(profile.get(field) not in (None, "") for field in ["name", "age", "weight", "height", "goal"])


@st.cache_resource
def _startup_db():
    init_db()


def ensure_state():
    _startup_db()
    if "aida_session" not in st.session_state:
        st.session_state.aida_session = create_session()
    if "aida_messages" not in st.session_state:
        st.session_state.aida_messages = []
    if "started_onboarding" not in st.session_state:
        st.session_state.started_onboarding = False

    session = st.session_state.aida_session
    if session.get("profile_id") is None:
        profile_id = latest_profile_id()
        if profile_id is not None:
            session["profile_id"] = profile_id
            session["mode"] = "assistant" if is_profile_complete(get_profile(profile_id)) else "onboarding"

    return session


def current_profile():
    session = ensure_state()
    profile_id = session.get("profile_id")
    return get_profile(profile_id) if profile_id is not None else None


def sidebar():
    profile = current_profile()
    st.sidebar.image("assets/logo.png", width=72)
    st.sidebar.markdown("### AiDa")
    st.sidebar.caption("Artificial Intelligence Daily Assistant")
    if profile:
        st.sidebar.markdown(f"**{profile.get('name') or 'Profile in progress'}**")
        st.sidebar.caption(profile.get("goal") or "Goal not set")
        st.sidebar.markdown(
            f'<span class="aida-pill">{icon("profile", 16)} Profile {"complete" if is_profile_complete(profile) else "in progress"}</span>',
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.caption("No profile yet")


def metric_data(profile_id):
    workouts = get_workout_sessions(profile_id) if profile_id else []
    meals = get_meals(profile_id) if profile_id else []
    weights = get_weight_logs(profile_id) if profile_id else []
    completed = sum(1 for row in workouts if row[6] == "completed")
    total = len(workouts)
    completion_rate = round((completed / total) * 100) if total else 0
    weight_change = None
    if len(weights) >= 2:
        weight_change = round(weights[-1][2] - weights[0][2], 1)
    return {
        "workouts": workouts,
        "meals": meals,
        "weights": weights,
        "completed": completed,
        "total": total,
        "completion_rate": completion_rate,
        "weight_change": weight_change,
    }


def render_card(title, body="", kicker=None, icon_name=None):
    icon_html = icon(icon_name, 20) if icon_name else ""
    kicker_html = f'<div class="aida-kicker">{kicker}</div>' if kicker else ""
    st.markdown(
        f"""
<div class="aida-card">
{kicker_html}
<h3>{icon_html} {title}</h3>
<div class="aida-label">{md.render(str(body))}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _encode_image_base64(path):
    """Read an image file and return a base64 data-URI string."""
    if not path or not os.path.exists(path):
        return None
    ext = os.path.splitext(path)[1].lstrip(".").lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{encoded}"


def render_messages(messages):
    for message in messages:
        role = message.get("role", "assistant")
        name = "You" if role == "user" else "AiDa"
        css_class = "aida-message-user" if role == "user" else "aida-message-ai"
        image_html = ""
        img_path = message.get("image_path")
        if img_path:
            data_uri = _encode_image_base64(img_path)
            if data_uri:
                image_html = f'<img class="aida-message-img" src="{data_uri}" alt="meal photo" />'
        st.markdown(
            f"""
<div class="{css_class}">
<div class="aida-message-name">{name}</div>
{image_html}
<div>{md.render(message.get("content", ""))}</div>
</div>
""",
            unsafe_allow_html=True,
        )


def seed_recent_messages():
    profile = current_profile()
    if not profile or st.session_state.aida_messages:
        return
    rows = get_recent_conversations(profile["id"], limit=6)
    for user_message, ai_response in rows:
        st.session_state.aida_messages.append({"role": "user", "content": user_message})
        st.session_state.aida_messages.append({"role": "assistant", "content": ai_response})


def ask_aida(user_message, mode=None, image_path=None):
    session = ensure_state()
    if mode:
        set_mode(session, mode)
    user_msg = {"role": "user", "content": user_message}
    if image_path:
        user_msg["image_path"] = image_path
    st.session_state.aida_messages.append(user_msg)
    try:
        with st.spinner("AiDa is thinking..."):
            response = process_message(user_message, session, image_path=image_path)
    except Exception as exc:
        response = (
            "I couldn't complete that request right now. "
            "Check your Gemini API configuration and try again.\n\n"
            f"Technical detail: {exc}"
        )
    st.session_state.aida_messages.append({"role": "assistant", "content": response})
    return response


def save_upload(uploaded_file):
    if uploaded_file is None:
        return None
    suffix = os.path.splitext(uploaded_file.name)[1] or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        return tmp.name


def workouts_dataframe(workouts):
    return pd.DataFrame(
        [
            {
                "id": row[0],
                "week_start": row[2],
                "day": row[3],
                "workout_name": row[4],
                "workout_details": row[5],
                "status": row[6],
            }
            for row in workouts
        ]
    )


def meals_dataframe(meals):
    return pd.DataFrame(
        [
            {
                "id": row[0],
                "description": row[2],
                "calories": row[3],
                "protein": row[4],
                "meal_type": row[5],
                "date": row[6],
            }
            for row in meals
        ]
    )


def weights_dataframe(weights):
    return pd.DataFrame(
        [{"id": row[0], "weight": row[2], "date": row[3]} for row in weights]
    )


def mark_completed(profile_id, day):
    return mark_workout_session_completed(profile_id, day)


def update_current_profile(data):
    profile = current_profile()
    if not profile:
        return False
    return update_profile(profile["id"], data)


def today_iso():
    return date.today().isoformat()
