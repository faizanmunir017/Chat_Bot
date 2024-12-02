import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")

    @classmethod
    def validate_config(cls):
        if not cls.CLAUDE_API_KEY or not cls.FRONTEND_ORIGIN:
            raise ValueError("Missing necessary environment variables")
