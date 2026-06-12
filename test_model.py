from google import genai
import json
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def test_extract():
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="hello"
        )
        print("flash works")
    except Exception as e:
        print("flash err:", e)

    try:
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it",
            contents="hello"
        )
        print("gemma worked")
    except Exception as e:
        print("gemma err:", type(e).__name__, e)

test_extract()
from agents.orchestrator import route_intent
print(f"route_intent result:", route_intent("Hi Aida, how are you today?"))
from agents.weight_agent import extract_weight_update
print(f"weight_update result:", extract_weight_update("Hi Aida, how are you today?"))
