from google import genai
from agents.llm_client import generate_with_fallback
from dotenv import load_dotenv
from google.genai import types
import json


load_dotenv()

def generate_workout(profile): 

    client = genai.Client()

    prompt = f"""
    You are experienced fitness coach.

    Generate a personalized weekly workout plan.
    User profile: 
    Age: {profile['age']}
    Weight: {profile['weight']}
    Height: {profile['height']}
    Goal: {profile['goal']}
    Workout equipment: {profile['workout_equipment']}
    Workout preferences: {profile['workout_preferences']}
    Health notes: {profile['health_notes']}

    Return ONLY valid JSON

    Required format:

    {{
    "week_plan": [
        {{
        "day": "Monday",
        "workout_name": "Upper Body",
        "workout_details": "Detailed exercises and sets"
        }}
    ],

    "display_text": "Human-readable workout plan"
    }}


    Rules: 
    -create a realistic weekly plan
    -adapt the plan to the user's informations
    -workout_name should be short
    -workout_details should contain exercises, sets and reps, or time if needed
    -display_text must be well formatted and easy to read, and well detailed so the user know what to do

    """

    config = types.GenerateContentConfig(
        response_mime_type="application/json"
    )

    response = generate_with_fallback(
        model="gemma-4-26b-a4b-it",
        contents=prompt,
        config=config
    )

    result = json.loads(response.text)

    if isinstance(result, list):

        if len(result) == 1:
            result = result[0]

        else:
            raise ValueError(
                "Unexpected list response"
            )

    return result

