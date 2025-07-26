from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.auth import decode_access_token
from backend.models.users import User
from backend.models.chat_history import ChatHistory

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    
    token = authorization.split(" ")[1]
    username = decode_access_token(token)
    
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

class ChatLog(BaseModel):
    question: str
    answer: str
    timestamp: datetime

    class Config:
        orm_mode = True

@router.get("/chat-history", response_model=List[ChatLog])
def get_chat_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user.username)
        .order_by(ChatHistory.timestamp.desc())
        .all()
    )
    return history
