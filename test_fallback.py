import os
from dotenv import load_dotenv
load_dotenv()

from agents.llm_client import generate_with_fallback, FALLBACK_MODELS

def test_fallback():
    print("Testing generate_with_fallback")
    
    # Temporarily prepend an invalid model to the fallback list and simulate a 503 error
    original_models = FALLBACK_MODELS.copy()
    FALLBACK_MODELS.insert(0, "gemini-2.5-flash-test-fail")
    
    # Monkey-patch the genai Client to simulate an error for the test model
    import google.genai
    original_client = google.genai.Client
    
    class FakeModels:
        def __init__(self, real_client):
            self.real_client = real_client
            
        def generate_content(self, model, contents, **kwargs):
            if model == "gemini-2.5-flash-test-fail":
                raise Exception("503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}")
            print(f"Calling real model: {model}")
            return self.real_client.models.generate_content(model=model, contents=contents, **kwargs)
            
    class FakeClient:
        def __init__(self):
            self.real_client = original_client()
            self.models = FakeModels(self.real_client)
            
    google.genai.Client = FakeClient
    
    try:
        response = generate_with_fallback(contents="Hello! Say 'Testing 1 2 3'")
        print(f"Response from fallback success: {response.text}")
    finally:
        google.genai.Client = original_client
        # Reset FALLBACK_MODELS
        FALLBACK_MODELS.clear()
        FALLBACK_MODELS.extend(original_models)

if __name__ == "__main__":
    test_fallback()
