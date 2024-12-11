from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    prompt: str
    