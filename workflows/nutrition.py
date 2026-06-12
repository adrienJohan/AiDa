from utils.nutrition_utils import (
    get_missing_nutrition_info,
    get_nutrition_question
)

from core.session import (
    get_profile_id,
    set_mode,
    set_waiting_for,
    clear_waiting_for,
    get_waiting_for
)

from memory.memory import (
    get_profile,
    update_profile,
    save_meals

)

from agents.meal_analyst_agent import analyze_meal_text

from agents.field_extractor import extract_field_answer

from agents.nutrition_agent import generate_meal_plan

from agents.image_meal_agent import analyze_meal_image

from agents.response_agent import humanize_response

from dotenv import load_dotenv
from google import genai

load_dotenv()


def handle_nutrition_mode( user_message, session, image_path=None):

    profile_id = get_profile_id(
        session
    )

    profile = get_profile(
        profile_id
    )

    waiting_for = get_waiting_for(
        session
    )

    #
    # We are answering a nutrition onboarding question
    #

    if waiting_for is not None:

        field_result = extract_field_answer(
            waiting_for,
            user_message
        )

        if not field_result["valid"]:

            return humanize_response(
                "The user gave an unclear answer to a nutrition onboarding question. Gently re-ask the question.",
                {
                    "field": waiting_for.replace('_', ' '),
                    "original_question": get_nutrition_question(waiting_for),
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

        clear_waiting_for(
            session
        )

        profile = get_profile(
            profile_id
        )

    #
    # Check missing nutrition information
    #

    missing_fields = (
        get_missing_nutrition_info(
            profile
        )
    )

    if missing_fields:

        next_field = (
            missing_fields[0]
        )

        set_waiting_for(
            session,
            next_field
        )

        return humanize_response(
            "AiDa needs to ask the user a question to learn about their nutrition plan preferences.",
            {
                "field": next_field.replace('_', ' '),
                "original_question": get_nutrition_question(next_field),
            },
        )

    #
    # Decide what nutrition task
    #

    if image_path is not None:
        nutrition_intent = "meal_image"
    else:
        nutrition_intent = (
            route_nutrition_request(
                user_message
            )
        )

    #
    # Meal plan
    #

    if nutrition_intent == "meal_plan":

        meal_plan = (
            generate_meal_plan(
                profile
            )
        )

        set_mode(
            session,
            "assistant"
        )

        return meal_plan

    #
    # Meal analysis
    #

    elif nutrition_intent == "meal_analysis":

        analysis = (
            analyze_meal_text(
                user_message
            )
        )

        save_meals(
            profile_id,
            analysis["description"],
            analysis["calories"],
            analysis["protein"],
            analysis["meal_type"],
            analysis["date"]
        )

        set_mode(
            session,
            "assistant"
        )

        return humanize_response(
            "The user just logged a meal via text. Summarize what was logged and give brief nutrition advice in a conversational way.",
            {
                "meal_description": analysis['description'],
                "meal_type": analysis['meal_type'],
                "date": analysis['date'],
                "estimated_calories": analysis['calories'],
                "estimated_protein": f"{analysis['protein']}g",
                "advice": analysis['advice'],
            },
        )
    
    elif nutrition_intent == "meal_image": 
        analysis = analyze_meal_image( image_path )

        save_meals(
            profile_id,
            analysis["description"],
            analysis["calories"],
            analysis["protein"],
            analysis["meal_type"],
            analysis["date"]          
        )

        set_mode(
            session,
            "assistant"
        )

        return humanize_response(
            "The user just uploaded a meal photo for analysis. Describe what was identified, share the nutrition estimates, and give brief advice conversationally.",
            {
                "meal_description": analysis['description'],
                "meal_type": analysis['meal_type'],
                "date": analysis['date'],
                "estimated_calories": analysis['calories'],
                "estimated_protein": f"{analysis['protein']}g",
                "advice": analysis['advice'],
            },
        )

    set_mode(
        session,
        "assistant"
    )

    return humanize_response(
        "The user said something related to nutrition but the intent was unclear. Ask them to clarify whether they want a meal plan, want to log a meal, or need nutrition advice.",
    )




def route_nutrition_request(
    user_message
):

    client = genai.Client()

    prompt = f"""
    Classify the nutrition request.

    Possible labels:

    meal_plan
    meal_analysis

    Rules:
    meal_plan:
    - create a meal plan
    - build a nutrition plan
    - suggest meals
    - help me eat for my goal

    meal_analysis:
    - user describes food they ate
    - user logs a meal
    - user asks about calories
    - user asks about protein

    
    Return ONLY one label.
    """

    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=user_message + "\n\n" + prompt
    )

    return response.text.strip().lower()
