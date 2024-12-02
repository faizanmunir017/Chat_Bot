from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Config
from controllers.chat_controller import chat_controller

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONTEND_ORIGIN],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_controller.router)


Config.validate_config()
