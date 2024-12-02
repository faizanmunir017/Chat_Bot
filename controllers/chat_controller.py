
from fastapi import APIRouter, HTTPException
from models.chat_model import ChatRequest
from services.chat_service import ChatService
from config import Config

class ChatController:
    def __init__(self):
        self.router = APIRouter()
        self.chat_service = ChatService(api_key=Config.CLAUDE_API_KEY)

        self.router.add_api_route("/chat", self.handle_chat_request, methods=["POST"])

    async def handle_chat_request(self, request: ChatRequest):
        try:
            result = self.chat_service.get_claude_response(request.prompt)
            return {"response": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


chat_controller = ChatController()

