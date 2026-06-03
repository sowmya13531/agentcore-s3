from rag.pdf_loader import load_pdf
from rag.chunker import chunk_text
from rag.embeddings import get_embedding
from rag.vector_store import collection

def build_index():
    if collection.count() > 0:
        return

    text = load_pdf("data/energy.pdf")
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[str(i)]
        )

def retrieve_chunks(question):
    query_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["documents"][0]