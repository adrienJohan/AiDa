from google import genai
from dotenv import load_dotenv
import os

load_dotenv()


client = genai.Client()

response = client.models.generate_content(
    model="gemma-4-26b-a4b-it",
    contents="Explain how AI works in ten words or less."
)


print(response.text)