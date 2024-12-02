from fastapi import APIRouter, HTTPException
from models.chat_model import ChatRequest
from services.gemini_service import GeminiService
from config import Config

class GeminiController:
    def __init__(self):
        self.router = APIRouter()
        self.gemini_service = GeminiService(api_key=Config.GEMINI_KEY)

        # Define routes
        self.router.add_api_route("/chat", self.chat_with_gemini, methods=["POST"])

    async def chat_with_gemini(self, request: ChatRequest):
        try:
            response = self.gemini_service.generate_response(request.prompt)
            return {"response": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Instantiate the controller
gemini_controller = GeminiController()
