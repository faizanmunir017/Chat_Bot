import os
from dotenv import load_dotenv

load_dotenv()  

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")
    LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY")

    @staticmethod
    def validate():
        
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
