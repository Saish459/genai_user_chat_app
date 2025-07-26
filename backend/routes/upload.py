from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Header
import os
from sqlalchemy.orm import Session
from backend.auth import decode_access_token
from backend.db import SessionLocal
from backend.models.users import User
from backend.file_ingest import extract_text_from_pdf, chunk_text
from backend.chroma_manager import add_to_chroma

router = APIRouter()

#Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Token-based User Extraction from Header
def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.split(" ")[1]
    username = decode_access_token(token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


#Upload Endpoint
@router.post("/upload")
def upload_pdf(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = user.username

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    user_folder = os.path.join("data", user_id)
    os.makedirs(user_folder, exist_ok=True)

    save_path = os.path.join(user_folder, file.filename)
    with open(save_path, "wb") as f:
        f.write(file.file.read())

    try:
        text = extract_text_from_pdf(save_path)
        chunks = chunk_text(text)
        add_to_chroma(chunks, user_id=user_id, filename=file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")

    return {"message": f"Uploaded and embedded {file.filename} for user {user_id}"}
