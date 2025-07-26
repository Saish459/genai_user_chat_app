import os
import sys

os.environ["CHROMA_TELEMETRY"] = "FALSE"

from backend.file_ingest import extract_text_from_pdf, chunk_text
from backend.chroma_manager import add_to_chroma

DATA_DIR = "data"

def embed_all_users():
    if not os.path.exists(DATA_DIR):
        print(f"Folder not found: {DATA_DIR}")
        sys.exit(1)

    for user_folder in os.listdir(DATA_DIR):
        user_path = os.path.join(DATA_DIR, user_folder)
        if not os.path.isdir(user_path):
            continue

        user_id = user_folder

        for filename in os.listdir(user_path):
            if not filename.endswith(".pdf"):
                continue

            full_path = os.path.join(user_path, filename)
            print(f"📄 Embedding {filename} for user: {user_id}")

            try:
                raw_text = extract_text_from_pdf(full_path)
                chunks = chunk_text(raw_text)
                add_to_chroma(chunks, user_id=user_id, filename=filename)
                print("")
            except Exception as e:
                print(f"Failed to process {filename} for {user_id}: {e}")

    print("All PDFs are embedded for all users.")

if __name__ == "__main__":
    embed_all_users()
