from memory.memory import ( 
    get_profile,
    get_meals,
    get_workout_sessions
)

from core.session import (
    get_profile_id,
    set_mode,
)

from agents.analyst_agent import analyze_progress
from agents.response_agent import humanize_response

def handle_analysis_mode( user_message, session ):

    profile_id = get_profile_id(session)

    if profile_id is None:

        set_mode(
            session,
            "assistant"
        )

        return humanize_response(
            "The user asked for a progress analysis but no profile exists yet. Let them know they need to complete onboarding first.",
        )

    profile = get_profile(profile_id)

    workout_sessions = get_workout_sessions(profile_id)
    print("workout sessions: ", workout_sessions)
    print()


    meals = get_meals(profile_id)
    print("meals: ", meals)

    analysis = analyze_progress(profile, workout_sessions, meals)

    set_mode(session, "assistant")

    return analysis