from backend.db import SessionLocal
from backend.auth import hash_password
from backend.models.users import User
from backend.models.chat_history import ChatHistory


db = SessionLocal()

username = "hemanth"
password = "SEtwo"

hashed = hash_password(password)
user = User(username=username, hashed_password=hashed)

db.add(user)
db.commit()
db.close()

print(f"✅ User {username} created with password {password}")