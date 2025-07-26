from backend.db import Base, engine

from backend.models.users import User
from backend.models.chat_history import ChatHistory

Base.metadata.create_all(bind=engine)
print("✅ ChatHistory table created.")