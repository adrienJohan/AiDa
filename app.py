import streamlit as st
import textwrap

from ui import (
    add_spacer,
    ask_aida,
    current_profile,
    ensure_state,
    icon,
    inject_css,
    is_profile_complete,
    metric_data,
    render_messages,
    sidebar,
)


st.set_page_config(
    page_title="AiDa",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
session = ensure_state()
sidebar()
profile = current_profile()


def render_landing():
    left, right = st.columns([1.4, 0.8], vertical_alignment="center")
    with left:
        st.markdown(
            f"""
<section class="aida-hero">
<div>
<div class="aida-kicker">{icon("logo", 18)} Artificial Intelligence Daily Assistant</div>
<h1>AiDa</h1>
<p class="aida-copy">
A calm fitness and nutrition workspace with an AI coach that remembers your goals,
builds plans, tracks progress, and helps you decide the next useful action.
</p>
</div>
</section>
""",
            unsafe_allow_html=True,
        )
        if st.button("Enter AiDa", type="primary", use_container_width=False):
            st.session_state.started_onboarding = True
            st.rerun()
    with right:
        st.image("assets/logo.png", use_container_width=True)


def render_onboarding():
    st.markdown("## Onboarding")
    st.markdown(
        "AiDa will collect the basics through conversation. Tell it what you can; you can keep answers short."
    )

    if not st.session_state.aida_messages:
        st.session_state.aida_messages.append(
            {
                "role": "assistant",
                "content": "Tell me about yourself and your fitness goals. Include your age, current weight, height, and what you want to achieve if you can.",
            }
        )

    render_messages(st.session_state.aida_messages)
    user_message = st.chat_input("Reply to AiDa")
    if user_message:
        ask_aida(user_message, mode="onboarding")
        st.rerun()


def recommended_action(profile, metrics):
    if not profile.get("workout_equipment") or not profile.get("workout_preferences"):
        return "Create a workout plan so AiDa can learn your equipment and training style."
    if metrics["total"] == 0:
        return "Create your first workout plan."
    if not profile.get("nutrition_preferences"):
        return "Create a meal plan so nutrition recommendations match your preferences."
    if len(metrics["meals"]) == 0:
        return "Log your first meal today."
    if len(metrics["weights"]) < 2:
        return "Update your weight to start a trend line."
    return "Ask AiDa for a weekly report."


def render_profile_complete():
    st.markdown("## Profile Complete")
    st.markdown(
        f"""
<div class="aida-card">
<div class="aida-kicker">{icon("check", 18)} Setup finished</div>
<h3>Welcome {profile.get("name")}</h3>
<div class="aida-label">Ready to begin your fitness journey?</div>
</div>
""",
        unsafe_allow_html=True,
    )
    add_spacer("1.5rem")
    if st.button("Go to Mission Control", type="primary"):
        st.session_state.profile_complete_seen = True
        st.rerun()


def render_mission_control():
    metrics = metric_data(profile["id"])
    st.markdown("## Mission Control")
    st.caption("What should I do next?")

    weight_delta = metrics["weight_change"]
    weight_change = "No trend yet" if weight_delta is None else f"{weight_delta:+.1f} kg"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Goal", profile.get("goal") or "Not set")
    col2.metric("Current Weight", f"{profile.get('weight') or 0:g} kg")
    col3.metric("Weight Change", weight_change)
    col4.metric("Workout Completion", f"{metrics['completion_rate']}%")

    st.markdown("### Recommended Next Step")
    st.markdown(
        f"""
<div class="aida-card">
<h3>{icon("logo", 20)} AiDa Recommendation</h3>
<div class="aida-label">{recommended_action(profile, metrics)}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    add_spacer("1rem")
    st.markdown("### Actions")
    action_cols = st.columns(6)
    if action_cols[0].button("Create Workout Plan", use_container_width=True):
        ask_aida("Create a workout plan for me.", mode="coach")
        st.switch_page("pages/Coach.py")
    if action_cols[1].button("Create Meal Plan", use_container_width=True):
        ask_aida("Create a meal plan for me.", mode="nutrition")
        st.switch_page("pages/Coach.py")
    if action_cols[2].button("Update Weight", use_container_width=True):
        st.switch_page("pages/Coach.py")
    if action_cols[3].button("Weekly Report", use_container_width=True):
        ask_aida("Give me my weekly report.", mode="weekly_report")
        st.switch_page("pages/Progress.py")
    if action_cols[4].button("Analyze Progress", use_container_width=True):
        response = ask_aida("Analyze my progress.", mode="analysis")
        st.session_state.latest_progress_analysis = response
        st.switch_page("pages/Progress.py")
    if action_cols[5].button("Talk To AiDa", use_container_width=True):
        st.switch_page("pages/Coach.py")

    st.markdown("### Today At A Glance")
    left, middle, right = st.columns(3)
    with left:
        st.markdown(
            f"""
<div class="aida-card">
<div class="aida-kicker">{icon("dumbbell", 18)} Workouts</div>
<div class="aida-metric">{metrics["completed"]}/{metrics["total"]}</div>
<div class="aida-label">completed planned sessions</div>
</div>
""",
            unsafe_allow_html=True,
        )
    with middle:
        st.markdown(
            f"""
<div class="aida-card">
<div class="aida-kicker">{icon("meal", 18)} Nutrition</div>
<div class="aida-metric">{len(metrics["meals"])}</div>
<div class="aida-label">logged meals</div>
</div>
""",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f"""
<div class="aida-card">
<div class="aida-kicker">{icon("progress", 18)} Tracking</div>
<div class="aida-metric">{len(metrics["weights"])}</div>
<div class="aida-label">weight check-ins</div>
</div>
""",
            unsafe_allow_html=True,
        )


if profile is None and not st.session_state.started_onboarding:
    render_landing()
elif profile is None or not is_profile_complete(profile):
    render_onboarding()
elif not st.session_state.get("profile_complete_seen", False):
    render_profile_complete()
else:
    render_mission_control()
