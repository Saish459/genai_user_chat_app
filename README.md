# GenAI Chat RAG App

GenAI User Chat RAG App is a secure, AI system that enables authenticated users to upload their own PDF documents and interact with a Large Language Model (LLM) that can answer questions based solely on the user's personal data.

This Proof of Concept (POC) demonstrates a complete architecture combining modern GenAI practices like Retrieval-Augmented Generation (RAG) with robust user isolation and secure backend logic.

## Features

- **User authentication** with JWT + hashed passwords
- **PDF upload & processing**, stored per user
- **RAG (Retrieval-Augmented Generation)** using ChromaDB + HuggingFace embeddings
- **LLM chat interface** LLaMA 4 via API)
- **User-specific Q&A** — responses are contextually restricted to the user’s documents
- **Frontend** in Streamlit + Chatlit / Chainlit / Next.js (POC variants)
- **PostgreSQL** for secure user login & chat history storage DB

## Tech Stack

| Layer        | Tools Used                                 |
|--------------|--------------------------------------------|
| Backend      | FastAPI, SQLAlchemy, JWT, bcrypt           |
| Vector DB    | ChromaDB (per-user isolated collections)   |
| Embeddings   | HuggingFace MiniLM                         |
| Auth         | OAuth2PasswordBearer, JWT, bcrypt          |
| LLM          | Meta LLaMa 4 Maverick                      |
| UI           | Streamlit                                  |
| Database     | PostgreSQL (user login & chat history)     |


## Project structure
```
genai-user-chat-rag/
├── app.py                        # Streamlit UI
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── README.md                    # Project overview
├── scripts/                     # One-time DB scripts
│   ├── add_user.py
│   └── create_chat_table.py
├── data/                        # User-specific PDF + embeddings
│   ├── user_test/
│   │   └── sample.pdf
│   └── ...
├── backend/
│   ├── main.py                  # FastAPI entrypoint
│   ├── auth.py                  # JWT auth & password utils
│   ├── db.py                    # SQLAlchemy session + engine
│   ├── file_ingest.py           # PDF reading, chunking
│   ├── chroma_manager.py        # ChromaDB setup per user
│   ├── chat_rag.py              # Core RAG logic using Groq
│   ├── models/
│   │   ├── user.py              # User table model
│   │   └── chat_history.py      # Chat history model
│   └── routes/
│       ├── auth.py              # /login endpoint
│       ├── chat.py              # /chat endpoint
│       ├── upload.py            # /upload endpoint
│       └── history.py           # /chat-history endpoint
```

## How It Works

1. User logs in (JWT generated)
2. User starts asking related questions or uploads a PDF → text extracted → embedded → stored in ChromaDB
3. User types a question → top relevant chunks retrieved → sent to LLM
4. LLM responds only based on *that user's* context


## Setup

```bash
git clone https://github.com/yourname/genai-user-chat-rag.git
cd genai-user-chat-rag

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Ensure PostgreSQL is running and create a **.env** file:

```bash
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/your_db

GROQ_API_KEY=your_groq_key
GROQ_MODEL=meta-llama/llama-4-maverick-17b-128e-instruct
```

## Running the App

**Backend:**
```bash
uvicorn backend.main:app --reload
```

**Frontend:**
```bash
streamlit run app.py
```


