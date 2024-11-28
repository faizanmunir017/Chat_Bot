

#Chat Completion API : 
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware




load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
frontend_origin = os.getenv("FRONTEND_ORIGIN")

client=OpenAI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_with_gpt(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "I am a helpful AI chat bot."},
                {"role": "user", "content": request.prompt}
            ]
        )

        print("Response is : ", response)
        return {"response": response.choices[0].message.content}
    except Exception as e:
       
       print(e)
       
       raise HTTPException(status_code=500, detail=str(e))

