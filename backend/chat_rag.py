import os
from groq import Groq
from backend.chroma_manager import get_user_retriever

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = os.getenv("GROQ_MODEL")

def run_chat(question: str, user_id: str) -> str:
    retriever = get_user_retriever(user_id)
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    system_prompt = """
        You are a reliable AI assistant that only answers using the provided context.
        Instructions:
        - Use ONLY the provided context to answer.
        - Do NOT answer from general knowledge.
        - If the answer is not present in the context, say: "I don't know."
        - Be honest, concise, and helpful.
        - Avoid hallucinating or fabricating information.
    """

    user_prompt = f"""
        Context: {context}

        Question: {question}
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ],
        temperature=0.3,
        max_tokens=1024,
        top_p=1,
    )

    return response.choices[0].message.content.strip()