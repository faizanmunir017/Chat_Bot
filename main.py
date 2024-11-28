import google.generativeai as genai
import os
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

geminiKey=os.getenv("GEMINI_KEY")
frontend_origin=os.getenv("FRONTEND_ORIGIN")

print(geminiKey)

app=FastAPI()


class ChatRequest(BaseModel):
    prompt: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_with_gemini(prompt:ChatRequest):

    try:
        genai.configure(api_key=geminiKey)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt.prompt)
        print(response.text)
        return {"response":response.text}

    except Exception as e:
        print(f"Error occured : {e}")







