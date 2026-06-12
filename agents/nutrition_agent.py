from google import genai
from agents.llm_client import generate_with_fallback
from dotenv import load_dotenv


load_dotenv()

def generate_meal_plan(profile):

    client = genai.Client()

    prompt = f"""
    You are an experienced nutrition coach

    User information: 
    Age: {profile['age']}
    Weight: {profile['weight']}
    Height: {profile['height']}
    Goal: {profile['goal']}
    Nutrition preferences: {profile['nutrition_preferences']}

    Generate a realistic meal plan.

    Make the meal plan realistic and adapted to user's profile
    """

    response = generate_with_fallback(
        model="gemma-4-26b-a4b-it",
        contents=prompt
    )

    return response.text



