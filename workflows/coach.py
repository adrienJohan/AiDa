from memory.memory import (
    get_profile,
    update_profile,
    save_workout_plan, 
    mark_workout_session_completed,
    get_today_name

)

from core.session import (
    get_profile_id,
    set_mode,
    set_waiting_for,
    clear_waiting_for,
    get_waiting_for, 
    get_pending_intent, 
    set_pending_intent, 
    clear_pending_intent
)

from utils.workout_utils import (
    get_missing_workout_info,
    get_workout_question
)

from agents.field_extractor import extract_field_answer

from agents.workout_agent import generate_workout

from agents.workout_completion_agent import extract_completed_day

from agents.response_agent import humanize_response

from google import genai

from dotenv import load_dotenv

load_dotenv()



def handle_coach_mode( user_message, session ):

    profile_id = get_profile_id( session )

    profile = get_profile( profile_id )

    waiting_for = get_waiting_for( session )

    #
    # We are waiting for a coach onboarding answer
    #

    if waiting_for is not None:

        field_result = extract_field_answer(
            waiting_for,
            user_message
        )

        if not field_result["valid"]:

            return humanize_response(
                "The user gave an unclear answer to a coach onboarding question. Gently re-ask the question.",
                {
                    "field": waiting_for.replace('_', ' '),
                    "original_question": get_workout_question(waiting_for),
                },
            )

        profile_data = {
            waiting_for:
            field_result["value"]
        }

        update_profile(
            profile_id,
            profile_data
        )

        clear_waiting_for( session )

        profile = get_profile(
            profile_id
        )

    #
    # Check missing workout information
    #

    missing_fields = (
        get_missing_workout_info( profile )
    )

    if missing_fields:

        #
        # Save original intent only once
        #

        if get_pending_intent(
            session
        ) is None:

            coach_intent = (
                route_coach_request(
                    user_message
                )
            )

            set_pending_intent(
                session,
                coach_intent
            )

        next_field = (
            missing_fields[0]
        )

        set_waiting_for(
            session,
            next_field
        )

        return get_workout_question(
            next_field
        )
    #
    # Coach intent routing
    #

    coach_intent = (
        get_pending_intent(session)
    )

    if coach_intent is None: 
        coach_intent = route_coach_request(user_message)


    #
    # Workout completion
    #

    if coach_intent == "workout_completion":

        completion = (
            extract_completed_day( user_message )
        )

        if not completion["valid"]:

            return humanize_response(
                "The user tried to mark a workout as completed but the message was unclear. Ask them to clarify which day's workout they completed.",
            )

        day = completion["day"]

        if day == "today":
            day = get_today_name()

        updated = (
            mark_workout_session_completed(
                profile_id,
                day
            )
        )

        clear_pending_intent(session)

        set_mode(
            session,
            "assistant"
        )

        if updated == 0:

            return humanize_response(
                "The user tried to mark a workout as completed but no planned workout exists for that day.",
                {"day": day},
            )

        return humanize_response(
            "The user just completed a workout. Congratulate them naturally and confirm it's been logged.",
            {"day": day},
        )

    #
    # Workout generation
    #

    elif coach_intent == "workout_plan":

        workout = generate_workout(
            profile
        )

        save_workout_plan(
            profile_id,
            workout["week_plan"]
        )

        clear_pending_intent( session )

        set_mode(
            session,
            "assistant"
        )

        return workout["display_text"]

    #
    # Fallback
    #

    set_mode(
        session,
        "assistant"
    )

    return humanize_response(
        "The user said something related to workouts but it's unclear if they want a new plan or are logging a completed workout. Ask them to clarify.",
    )

def route_coach_request( user_message) : 
    client = genai.Client()

    prompt = f"""
    Classify the user's coach request.

    Possible labels:

    workout_plan
    workout_completion

    Rules:

    workout_plan:
    - create a workout plan
    - build a training plan

    workout_completion:
    - completed workout
    - finished workout
    - did my workout
    - completed Monday workout
    - completed today's workout

    Return ONLY one label.
    """

    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=user_message + "\n\n" + prompt
    )

    return response.text.strip().lower()

