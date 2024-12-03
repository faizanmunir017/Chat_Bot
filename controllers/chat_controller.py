from fastapi import APIRouter, HTTPException
from models.chat_model import ChatRequest
from services.chat_service import ChatService
from config import Config

class ChatController:
    def __init__(self):
        self.router = APIRouter()
        self.chat_service = ChatService(api_key=Config.OPENAI_API_KEY)
        self.router.add_api_route("/chat", self.chat_with_gpt, methods=["POST"])

    async def chat_with_gpt(self, request: ChatRequest):
        try:
            result = self.chat_service.chat_with_gpt(request.prompt)
            print("result is ",result)
            return {"response": result}
        except Exception as e:
            
                
            print(f"Error in chat_with_gpt: {e}")  # Log the exception
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        
chat_controller = ChatController()
