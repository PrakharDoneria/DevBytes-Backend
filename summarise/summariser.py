import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI API
genai.configure(api_key=GEMINI_API_KEY)

# Model Configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="Your task is to summarize the news into 60 words or less. Return only the summarized text.",
)

def summarise(text: str) -> str:
    """Summarizes the given news text."""
    if not text:
        return "No input provided."

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(text)
    return response.text.strip()