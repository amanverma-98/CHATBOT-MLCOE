import os
import pandas as pd
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

def load_documents(directory):
    documents = []

    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            documents.extend(loader.load())

        elif file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                documents.append(Document(page_content=f.read()))

        elif file.endswith(".csv"):
            df = pd.read_csv(path)
            documents.append(Document(page_content=df.to_string()))

    return documents
