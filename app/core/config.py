import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
VECTORSTORE_PATH = os.path.join(BASE_DIR, "data", "vectorstore")
DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
DATABASE_URL = "sqlite:///./mlcoe.db"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")