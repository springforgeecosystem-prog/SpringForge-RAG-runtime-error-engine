from embeddings import generate_embedding
from vectorstore import vector_search

def retrieve_context(error_text: str, k: int = 5):
    """
    Embed the error text, then retrieve top-k similar docs
    """
    error_embedding = generate_embedding(error_text) 

    return vector_search(
        embedding=error_embedding,
        top_k=k
    )
