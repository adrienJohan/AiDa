import streamlit as st

from ui import (
    ask_aida,
    current_profile,
    ensure_state,
    icon,
    inject_css,
    meals_dataframe,
    metric_data,
    save_upload,
    sidebar,
)


st.set_page_config(
    page_title="Nutrition | AiDa",
    page_icon="assets/logo.png",
    layout="wide",
)

inject_css()
ensure_state()
sidebar()
profile = current_profile()

st.markdown("## Nutrition")

if not profile:
    st.info("Start onboarding from the AiDa home page first.")
    st.page_link("app.py", label="Go to AiDa Home")
    st.stop()

metrics = metric_data(profile["id"])
meals = metrics["meals"]
df = meals_dataframe(meals)

calories = int(df["calories"].sum()) if not df.empty else 0
protein = int(df["protein"].sum()) if not df.empty else 0

cols = st.columns(4)
cols[0].metric("Logged Meals", len(meals))
cols[1].metric("Calories Logged", calories)
cols[2].metric("Protein Logged", f"{protein}g")
cols[3].metric("Preference", profile.get("nutrition_preferences") or "Not set")

st.markdown("### Meal Strategy")
strategy_cols = st.columns(4)
for col, title, body in [
    (strategy_cols[0], "Breakfast", "Prioritize protein and slow carbohydrates."),
    (strategy_cols[1], "Lunch", "Build a balanced plate around your goal."),
    (strategy_cols[2], "Dinner", "Keep it satisfying and easy to repeat."),
    (strategy_cols[3], "Snack", "Use snacks to close protein or energy gaps."),
]:
    with col:
        st.markdown(
            f"""
            <div class="aida-card">
                <div class="aida-kicker">{icon("meal", 18)}</div>
                <h3>{title}</h3>
                <div class="aida-label">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

action_cols = st.columns(3)
if action_cols[0].button("Create Meal Plan", use_container_width=True):
    ask_aida("Create a meal plan for me.", mode="nutrition")
    st.switch_page("pages/Coach.py")
if action_cols[1].button("Log Meal", use_container_width=True):
    st.session_state.show_meal_form = True
if action_cols[2].button("Analyze Meal Photo", use_container_width=True):
    st.session_state.show_photo_form = True

if st.session_state.get("show_meal_form"):
    with st.form("nutrition_meal_form", clear_on_submit=True):
        meal = st.text_area("Meal", placeholder="For dinner I ate steak and vegetables.")
        submitted = st.form_submit_button("Analyze And Log")
    if submitted and meal.strip():
        st.session_state.show_meal_form = False
        ask_aida(meal, mode="nutrition")
        st.rerun()

if st.session_state.get("show_photo_form"):
    uploaded = st.file_uploader("Meal photo", type=["jpg", "jpeg", "png"])
    camera = st.camera_input("Take a meal photo")
    image = uploaded or camera
    if image is not None and st.button("Analyze Photo", type="primary"):
        path = save_upload(image)
        st.session_state.show_photo_form = False
        ask_aida("Analyze this meal photo.", mode="nutrition", image_path=path)
        st.rerun()

st.markdown("### Logged Meals")
if df.empty:
    st.markdown(
        """
        <div class="aida-card">
            <h3>No meals logged yet</h3>
            <div class="aida-label">Log a meal from this page or ask AiDa in Coach.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.dataframe(
        df[["date", "meal_type", "description", "calories", "protein"]],
        use_container_width=True,
        hide_index=True,
    )
