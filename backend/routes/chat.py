from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.auth import decode_access_token
from backend.models.users import User
from backend.chat_rag import run_chat
from backend.models.chat_history import ChatHistory

from fastapi.security.api_key import APIKeyHeader
from fastapi import APIRouter, Depends, HTTPException

api_key_header = APIKeyHeader(name="Authorization")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str


def get_current_user(
    token: str = Depends(api_key_header),
    db: Session = Depends(get_db)
):
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    jwt = token.split(" ")[1]
    username = decode_access_token(jwt)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user



@router.post("/chat", response_model=ChatResponse)
def chat(
    chat_request: ChatRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    answer = run_chat(chat_request.question, user_id=user.username)

    chat_log = ChatHistory(
        user_id=user.username,
        question=chat_request.question,
        answer=answer
    )
    db.add(chat_log)
    db.commit()

    return {"answer": answer}