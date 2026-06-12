from google import genai
from agents.llm_client import generate_with_fallback
from dotenv import load_dotenv

from utils.analysis_utils import format_workout_sessions, format_meals

load_dotenv()


def analyze_progress(
    profile,
    workout_sessions,
    meals
):

    client = genai.Client()

    formatted_workouts = format_workout_sessions(workout_sessions)

    completed = sum(1 for session in workout_sessions if session[6] == "completed")

    total_sessions = len( workout_sessions )



    formatted_meals = format_meals(meals)

    prompt = f"""
    You are an expert fitness and nutrition analyst.

    User profile:

    Name: {profile['name']}
    Age: {profile['age']}
    Weight: {profile['weight']}
    Height: {profile['height']}
    Goal: {profile['goal']}
    Workout preferences: {profile['workout_preferences']}
    Nutrition preferences: {profile['nutrition_preferences']}
    Health notes: {profile['health_notes']}

    Workout stats: 
    total planned sessions: {total_sessions}
    completed sessions: {completed}
    workout sessions: {formatted_workouts}
    
    
    Meal history: {formatted_meals}

    Analyze the user's progress.

    Rules:

    - Do not simply repeat the raw data.
    - Identify patterns.
    - Identify strengths.
    - Identify weaknesses.
    - Give actionable recommendations.
    - If there is not enough data,
      explain what additional data would
      improve the analysis.
    - Be realistic.
    - do not mention any new data type needed for improved analysis(eg: sleep data, strength metrics...)

    Structure your response with:

    1. Overview
    2. Observations
    3. Recommendations
    """

    print(len(prompt))

    response = generate_with_fallback(
        model="gemma-4-26b-a4b-it",
        contents=prompt
    )

    return response.text