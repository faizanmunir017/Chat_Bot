from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Config
from controllers.chat_controller import chat_controller


try:
    Config.validate()  
except EnvironmentError as e:
    print(f"Configuration Error: {e}")
    exit(1)  

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_controller.router)


