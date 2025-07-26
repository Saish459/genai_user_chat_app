from sqlalchemy import Column, Integer, String
from backend.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

    # Reference ChatHistory after it's defined
    chats = relationship("ChatHistory", back_populates="user")
