import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_KEY = os.getenv("GEMINI_KEY")
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")

    if not GEMINI_KEY:
        raise ValueError("GEMINI_KEY is not set in environment variables.")
    if not FRONTEND_ORIGIN:
        raise ValueError("FRONTEND_ORIGIN is not set in environment variables.")
