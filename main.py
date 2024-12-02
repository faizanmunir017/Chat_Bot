from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.gemini_controller import gemini_controller
from config import Config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gemini_controller.router)