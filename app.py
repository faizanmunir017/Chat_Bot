
import os
import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

claude_api_key=os.getenv("CLAUDE_API_KEY")
frontend_origin = os.getenv("FRONTEND_ORIGIN")

print(f"Claude key is : {claude_api_key}")
print(f"Frontend origin is : {frontend_origin}")



app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt:str

@app.post("/chat")
async def chat_with_claude(request:ChatRequest):

    client = anthropic.Anthropic(
        api_key=claude_api_key,
    )
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": request.prompt}
        ]
    )

    return message.content[0].text