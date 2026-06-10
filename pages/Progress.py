import streamlit as st

from ui import (
    ask_aida,
    current_profile,
    ensure_state,
    icon,
    inject_css,
    metric_data,
    render_messages,
    sidebar,
    weights_dataframe,
)


st.set_page_config(
    page_title="Progress | AiDa",
    page_icon="assets/logo.png",
    layout="wide",
)

inject_css()
ensure_state()
sidebar()
profile = current_profile()

st.markdown("## Progress")

if not profile:
    st.info("Start onboarding from the AiDa home page first.")
    st.page_link("app.py", label="Go to AiDa Home")
    st.stop()

metrics = metric_data(profile["id"])
weight_delta = metrics["weight_change"]
weight_change = "No trend yet" if weight_delta is None else f"{weight_delta:+.1f} kg"

cols = st.columns(4)
cols[0].metric("Current Weight", f"{profile.get('weight') or 0:g} kg")
cols[1].metric("Weight Change", weight_change)
cols[2].metric("Workout Completion", f"{metrics['completion_rate']}%")
cols[3].metric("Meals Logged", len(metrics["meals"]))

st.markdown("### Weight Trend")
weights_df = weights_dataframe(metrics["weights"])
if weights_df.empty:
    st.markdown(
        """
        <div class="aida-card">
            <h3>No weight trend yet</h3>
            <div class="aida-label">Update your weight twice to see the trend line.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    chart_df = weights_df.set_index("date")[["weight"]]
    st.line_chart(chart_df, use_container_width=True)

st.markdown("### Weekly Report")
report_messages = [
    message for message in st.session_state.get("aida_messages", [])
    if message.get("role") == "assistant" and "weekly" in message.get("content", "").lower()
]

if st.button("Generate Weekly Report", type="primary"):
    ask_aida("Give me my weekly report.", mode="weekly_report")
    st.rerun()

if report_messages:
    st.markdown(
        f"""
        <div class="aida-card">
            <div class="aida-kicker">{icon("progress", 18)} Latest Report</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_messages([report_messages[-1]])
else:
    st.markdown(
        """
        <div class="aida-card">
            <h3>No weekly report yet</h3>
            <div class="aida-label">Generate one after logging workouts, meals, or weight updates.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
