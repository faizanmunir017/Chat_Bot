import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")

    @staticmethod
    def validate():
        """
        Check if all required environment variables are loaded.
        Raises an exception if any are missing.
        """
        missing_keys = []
        required_keys = ["OPENAI_API_KEY", "FRONTEND_ORIGIN"]
        
        for key in required_keys:
            if not os.getenv(key):
                missing_keys.append(key)
        
        if missing_keys:
            raise EnvironmentError(
                f"The following environment variables are missing or not loaded: {', '.join(missing_keys)}"
            )
        print("All required environment variables are loaded successfully.")
