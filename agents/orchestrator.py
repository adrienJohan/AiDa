




from google import genai
from dotenv import load_dotenv
from workflows.onboarding import handle_onboarding
from workflows.coach import handle_coach_mode
from workflows.nutrition import handle_nutrition_mode
from workflows.analysis import handle_analysis_mode
from workflows.weight_update import handle_weight_update
from workflows.weekly_report import handle_weekly_report
from memory.memory import save_conversation
from core.session import (
    get_profile_id,
    set_mode,
    get_mode,
)


load_dotenv()





def process_message(user_message, session, image_path=None):

    mode = get_mode(session)

    response = None

    if mode == "onboarding":

        response = handle_onboarding( user_message, session )

    elif mode == "assistant":

        response = handle_assistant_mode( user_message, session )

    elif mode == "coach":

        response = handle_coach_mode( user_message, session )

    elif mode == "nutrition":

        response = handle_nutrition_mode(
            user_message,
            session,
            image_path=image_path
        )

    elif mode == "analysis":

        response = handle_analysis_mode( user_message,session )

    elif mode == "weight_update": 
        response = handle_weight_update(user_message, session )
    
    elif mode == "weekly_report": 
        response = handle_weekly_report(session)

    else:

        response = "Unknown mode."

    profile_id = get_profile_id(session)

    if profile_id is not None and response:

        save_conversation( profile_id, user_message, response )

    return response


def handle_assistant_mode(user_message, session):

    intent = route_intent(user_message)

    if intent == "coach":

        set_mode(session, "coach")

        return handle_coach_mode(
            user_message,
            session
        )

    elif intent == "nutrition":

        set_mode(session, "nutrition")

        return handle_nutrition_mode(
            user_message,
            session
        )

    elif intent == "analysis":

        set_mode(session, "analysis")

        return handle_analysis_mode(
            user_message,
            session
        )
    
    elif intent == "weight_update": 

        set_mode(session, "weight_update")

        return handle_weight_update(
            user_message,
            session
        )
    
    elif intent == "weekly_report": 

        set_mode(session, "weekly_report")

        return handle_weekly_report(session)

    else:

        return (
            "I'm here to help. "
            "You can ask me about workouts, nutrition or progress analysis."
        )


def route_intent(user_message):

    client = genai.Client()

    prompt = f"""
    Classify the user's request.

    Possible labels:

    coach
    nutrition
    analysis
    weight_update
    weekly_report
    assistant

    Rules:

    coach:
    - workout plans
    - exercise advice
    - fitness training
    - maybe workout completion also(example: the user completed some workout)
    
    nutrition:
    - meal plans
    - calories
    - food advice
    - protein

    analysis:
    - progress analysis
    - trends
    - workout consistency

    assistant:
    - greetings
    - casual conversation
    - anything else

    weight_update example:
    - I weight 87kg, my weight is 86.5kg, I am down to 85kg

    weekly_report:
    - weekly report
    - progress report
    - generate report
    - weekly summary
    - summarize my progress
    - give me my report

    Return ONLY one label.

    User:
    {user_message}
    """

    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=prompt
    )

    return response.text.strip().lower()

