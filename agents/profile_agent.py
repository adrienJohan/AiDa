from google import genai
from google.genai import types
import json


def run():
    pass


def profile_agent(user_message): 

    client = genai.Client()

    system_instruction = """
        You are AiDa's profile extraction assistant. 

        Extract the following information from user's message:
        - name(TEXT)
        - age(INTEGER)
        - weight(REAL)
        - height(REAL)
        - goal(TEXT)
        - workout_equipment(TEXT)
        - workout_preferences(TEXT)
        - nutrition_preferences(TEXT)
        - health_notes(TEXT)
        - aida_notes(TEXT)
        
        Rules: 
        -return ONLY valid JSON
        -if a field is missing, return null
        -standardize height to centimeters, weight to kilograms
        -store non-structured observations in aida_notes
        -if information is inferred, mention it in aida_notes.
    """

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json"       
    )

    response = client.models.generate_content(
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