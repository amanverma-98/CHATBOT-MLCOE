from langchain.embeddings import HuggingFaceInferenceEmbeddings
import os

def get_embeddings():
    return HuggingFaceInferenceEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        hf_api_key=os.getenv("HF_TOKEN")
    )
