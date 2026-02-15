from langchain_groq import ChatGroq
from app.core.config import GROQ_API_KEY

def get_llm(streaming=False):
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.1-8b-instant",
        temperature=0.3,
        streaming=streaming
    )
