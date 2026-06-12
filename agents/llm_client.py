from google import genai
import logging

# We will fallback through these models in order
FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemma-4-31b-it",
    "gemma-4-26b-a4b-it"
]

def generate_with_fallback(contents, **kwargs):
    """
    Attempts to generate content using the standard priority pipeline of LLM models.
    Falls back to the next available model if a 503 (Unavailable) or 429 (Quota Exhausted) occurs.
    """
    client = genai.Client()
    
    last_error = None
    
    # Remove any specific model from kwargs since we handle it here
    if "model" in kwargs:
        del kwargs["model"]
        
    for model in FALLBACK_MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                **kwargs
            )
            return response
            
        except Exception as e:
            last_error = e
            error_str = str(e)
            
            # Check for availability / overload errors
            if "503" in error_str or "UNAVAILABLE" in error_str or "429" in error_str or "exhausted" in error_str.lower() or "500" in error_str or "INTERNAL" in error_str:
                logging.warning(f"Model {model} failed with {error_str}. Falling back to next model.")
                continue
            else:
                # For any other errors (like invalid prompt), do not fallback, re-raise immediately.
                raise e
                
    # If we exhaust all models
    raise Exception(f"All fallback models failed. Last error: {last_error}")
