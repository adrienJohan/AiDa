from google import genai
from agents.llm_client import generate_with_fallback
from google.genai import types
import json


def extract_completed_day( user_message ):

    client = genai.Client()

    system_instruction = """
    You extract workout completion information.

    Return ONLY valid JSON.

    Format:

    {
        "valid": true,
        "day": "Monday"
    }

    or

    {
        "valid": true,
        "day": "today"
    }

    or

    {
        "valid": false,
        "day": null
    }

    Rules:

    - valid=true only if the user indicates a workout was completed.
    - day must be one of:
    Monday
    Tuesday
    Wednesday
    Thursday
    Friday
    Saturday
    Sunday
    today

    - Return JSON only.
    """

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json"
    )

    response = generate_with_fallback(
        model="gemma-4-26b-a4b-it",
        contents=user_message,
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