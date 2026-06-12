from google import genai
from agents.llm_client import generate_with_fallback
from google.genai import types
import json
from dotenv import load_dotenv
from datetime import date

load_dotenv()


def analyze_meal_text( meal_description ):

    today = date.today()


    client = genai.Client()

    system_instruction = f"""
    You are a nutrition analyst.

    Current date: {today.isoformat()} (so you can know today and yesterday)

    Analyze the meal description.

    Return ONLY valid JSON.

    Format:

    
        "description": "Chicken and rice",
        "meal_type": "breakfast/lunch/snack/dinner",
        "date": "2026-06-09"
        "calories": number,
        "protein": number,
        "advice": "..."
    

    Rules: 
    meal_type must be one of: breakfast,lunch,dinner,snack,unknown

    if the meal type is not mentioned, use unknown

    if the user mentions: today, yesterday, infer the correct date

    If no date is provided, use today's date.

    Estimate calories and protein as realistically as possible.
    """

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json"
    )

    response = generate_with_fallback(
        model="gemma-4-26b-a4b-it",
        contents=meal_description,
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