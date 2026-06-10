import json 


from google import genai
from google.genai import types

from dotenv import load_dotenv


load_dotenv()


def extract_weight_update(user_message): 
    client = genai.Client()

    system_instruction = """
        You extract weight updates

        return ONLY valid JSON

        Format: 
        {
            "valid": true,
            "weight": 87
        }

        or
        {
            "valid": false,
            "weight": null
        }

        rules: 
        -a valid=true only if the user is reporting their current weight
        -weight must be numeric
    
    """

    config = types.GenerateContentConfig(
        system_instruction = system_instruction, 
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