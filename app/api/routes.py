from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from app.services.rag_service import generate_stream
import os
import shutil
from app.schemas.chat import ChatRequest

router = APIRouter()

UPLOAD_DIR = "app/data/raw"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "File uploaded"}

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generator():
        print("Received request:", request.model_dump())
        async for chunk in generate_stream(request.question, session_id="default_user"):
            yield chunk.encode("utf-8")

    return StreamingResponse(generator(), media_type="text/plain")
