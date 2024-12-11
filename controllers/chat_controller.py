from fastapi import APIRouter, HTTPException, Request,Depends
from models.chat_model import ChatRequest
from services.chat_service import ChatService
from config import Config
from slowapi import Limiter
from slowapi.util import get_remote_address
from langchain_core.vectorstores import InMemoryVectorStore


limiter = Limiter(key_func=get_remote_address)

class ChatController:
    def __init__(self, limiter: Limiter,vector_store:InMemoryVectorStore):
        self.router = APIRouter()
        self.chat_service = ChatService(api_key=Config.OPENAI_API_KEY, vector_store=vector_store)
        self.limiter = limiter
        self.vector_store=vector_store

        self.router.add_api_route(
            "/chat", 
            self.chat_with_gpt, 
            methods=["POST"],
        )

    async def chat_with_gpt(
        self, 
        request: ChatRequest, 
        current_request: Request
    ):
        try:
            current_request.state.limiter = self.limiter
            
            result = await self.chat_service.chat_with_gpt(request.prompt)
            
            return {"response":result}
        
        except Exception as e:
            print(f"Error in chat_with_gpt: {e}") 
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        

def create_chat_controller(limiter, vector_store):
    return ChatController(limiter, vector_store)