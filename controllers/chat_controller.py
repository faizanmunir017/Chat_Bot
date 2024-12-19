from fastapi import APIRouter, HTTPException, Request,Depends
from models.user_prompt_schema import ChatRequest
from services.chat_service import ChatService
from config.env_validation import Config
from slowapi import Limiter
from slowapi.util import get_remote_address
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.schema.retriever import BaseRetriever
from config.db import get_database
from utils.chat_helper import get_last_messages

limiter = Limiter(key_func=get_remote_address)

class ChatController:
    def __init__(self, limiter: Limiter,vector_store:InMemoryVectorStore,retriever:BaseRetriever):
        self.router = APIRouter()
        self.limiter = limiter
        self.vector_store=vector_store
        self.retriever=retriever

        db=get_database()
        messages_collection=db["Messages"]

        self.chat_service = ChatService(api_key=Config.OPENAI_API_KEY, vector_store=vector_store,retriever=retriever,db_collection=messages_collection)

        self.router.add_api_route(
            "/chat", 
            self.chat_with_gpt, 
            methods=["POST"],
        )

        self.router.add_api_route(
            "/chat",
            self.get_last_messages,
            methods=["GET"],
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
        
    async def get_last_messages(self):

        try:
            messages= await get_last_messages(self.chat_service.collection)

            if not messages:
                return {"messages":[]}
            
            return {"messages":messages}

        except Exception as e:
            print("Error in getting Startup messages from database")
        
def create_chat_controller(limiter, vector_store,retriever): 
    return ChatController(limiter, vector_store,retriever)