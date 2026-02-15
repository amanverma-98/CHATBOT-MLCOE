from app.services.vectorstore_service import load_vectorstore

def retrieve(question: str):
    vectorstore = load_vectorstore()
    if not vectorstore:
        return None, 1.0  # If no vectorstore, just return "no context"

    docs = vectorstore.similarity_search_with_score(question, k=3)
    if not docs:
        return None, 1.0

    best_doc, score = docs[0]

    return best_doc.page_content, score
