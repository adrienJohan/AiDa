from memory.memory import ( 
    get_profile, 
    get_workout_sessions, 
    get_meals, 
    get_weight_logs
)


from agents.weekly_report_agent import generate_weekly_report

from core.session import get_profile_id, set_mode


def handle_weekly_report(session): 

    profile_id = get_profile_id(session)

    profile = get_profile(profile_id)



    workouts = get_workout_sessions(profile_id)

    meals = get_meals(profile_id)

    weights = get_weight_logs(profile_id)

    weekly_report = generate_weekly_report(
        profile, 
        workouts, 
        meals, 
        weights
    )

    set_mode(session,"assistant")


    return weekly_report