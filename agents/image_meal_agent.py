from google import genai
from google.genai import types
import json
from datetime import date
from dotenv import load_dotenv

load_dotenv()

def analyze_meal_image( image_path ) : 
    client = genai.Client()

    today = date.today().isoformat()

    image = types.Part.from_bytes(
        data=open(
            image_path,
            "rb"
        ).read(),
        mime_type="image/jpeg"
    )

    prompt = f"""

    Current date: {today}

    Analyze the food shown in the image. Return ONLY valid JSON

    format: 
    {{
        "description": "...",
        "meal_type": "unknown",
        "date": "{today}",
        "calories": 650,
        "protein": 45,
        "advice": "..."
    }}

    Rules: 
    - Identify the meal
    - Estimate calories
    - Estimate protein
    - Keep meal_type as "unknown"
    - use today's date
    - description should not be too long(not more than 25 words)
    """ 

    config = types.GenerateContentConfig(
        response_mime_type="application/json"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            image,
            prompt
        ],
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