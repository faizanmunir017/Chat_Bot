from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import Config
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address


from controllers.chat_controller import create_chat_controller

try:
    Config.validate()  
except EnvironmentError as e:
    print(f"Configuration Error: {e}")
    exit(1)  


limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI()

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(429)
async def rate_limit_exceeded_handler(request: Request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."},
    )


chat_controller = create_chat_controller(limiter)


app.include_router(chat_controller.router)