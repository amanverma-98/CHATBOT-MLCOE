import os
from langchain_community.vectorstores import FAISS
from app.services.embedding_service import get_embeddings
from app.core.config import VECTORSTORE_PATH
from app.core.config import DATA_PATH

def create_vectorstore(documents):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(VECTORSTORE_PATH)

def load_vectorstore():
    embeddings = get_embeddings()
    if not os.path.exists(VECTORSTORE_PATH):
        raise ValueError("Vectorstore not found! Please run ingestion first.")
    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
