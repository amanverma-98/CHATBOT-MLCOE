from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes import router
from app.services.ingestion_service import load_documents
from app.services.chunking_service import chunk_documents
from app.services.vectorstore_service import create_vectorstore
from app.core.config import DATA_PATH

# Lifespan handler (modern replacement for on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INFO] Starting MLCoE Chatbot...")

    # Always rebuild vectorstore at startup
    documents = load_documents(DATA_PATH)
    chunks = chunk_documents(documents)
    create_vectorstore(chunks)

    print("[INFO] Vectorstore rebuilt successfully")

    yield  # App runs here

    print("[INFO] Shutting down MLCoE Chatbot...")

# Create FastAPI instance with lifespan
app = FastAPI(
    title="MLCoE Chatbot",
    lifespan=lifespan
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mlcoechatbot.vercel.app" , "https://chatbot-mlcoe-i2id.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "running"}
