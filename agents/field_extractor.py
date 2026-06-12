from google import genai
from agents.llm_client import generate_with_fallback
from google.genai import types
import json



def extract_field_answer( field, user_message):

    client = genai.Client()

    system_instruction = f"""
    You are extracting information for ONE field.

    Target field:
    {field}

    Analyze the user's answer.

    Return ONLY valid JSON. don't use markdown, ```json or any explanation

    Format:

    {{
        "valid": true,
        "value": "<extracted value>"
    }}

    or

    {{
        "valid": false,
        "value": null
    }}

    Rules:

    - valid=true only if the answer actually provides information for the target field.
    - valid=false if the answer is unrelated.
    - do not explain anything.

    For health_notes, the kind of following answers are valid:
    - none
    - no injuries
    - no conditions
    - healthy
    - nothing to report

    These should return valid=true.
    """

    config = types.GenerateContentConfig(
        system_instruction=system_instruction
    )

    response = generate_with_fallback(
        model="gemma-4-26b-a4b-it",
        contents=user_message,
        config=config
    )

    print(response.text)

    result = json.loads(response.text)

    if isinstance(result, list):

        if len(result) == 1:
            result = result[0]

        else:
            raise ValueError(
                "Unexpected list response"
            )

    return result