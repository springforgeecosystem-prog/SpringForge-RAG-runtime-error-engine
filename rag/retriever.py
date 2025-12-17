from vectorstore import vector_search

def retrieve_context(error_text: str, k: int = 5):
    """
    Returns top-k relevant docs from pgvector
    """
    return vector_search(
        embedding=error_text,
        top_k=k
    )
