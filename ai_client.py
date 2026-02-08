from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL

def get_ai_client():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set")
    return OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)
