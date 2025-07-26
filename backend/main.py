from fastapi import FastAPI
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import auth, chat, upload, chat_history

api_key_header = APIKeyHeader(name="Authorization")


app = FastAPI()

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(chat_history.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)