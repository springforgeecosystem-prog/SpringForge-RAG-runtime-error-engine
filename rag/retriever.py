# retriever.py
from rag.embeddings import generate_embedding
from rag.vectorstore import vector_search
from llm.generator import generate_fix 

def summarize_error_for_search(error_text: str) -> str:
    """
    Uses an LLM to turn a messy stack trace into a clean 1-sentence 
    technical summary for better vector retrieval.
    """
    prompt = f"""
    Analyze the following Java stack trace and output ONLY a 1-sentence technical 
    summary of the root cause. Focus on the specific Spring/Hibernate mechanism 
    failing (e.g., 'LazyInitializationException in Controller' or 'Circular Dependency').
    
    Error: {error_text[:2000]} # Limit text to avoid token waste
    """
    
    summary = generate_fix(prompt)
    return summary.strip() 

def retrieve_context(error_text: str, k: int = 5):
    """
    1. Summarize the error to remove noise.
    2. Embed the summary.
    3. Retrieve top-k similar docs.
    """
    # --- NEW STEP: SUMMARIZATION ---
    # This prevents 'JBoss' or 'Vaadin' links from showing up 
    # just because 'Spring' was mentioned in the stack trace.
    search_query = summarize_error_for_search(error_text)
    print(f"DEBUG: Searching for: {search_query}")

    # Embed the clean summary instead of the raw error
    error_embedding = generate_embedding(search_query) 

    return vector_search(
        embedding=error_embedding,
        top_k=k
    )