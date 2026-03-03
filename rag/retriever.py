import re
from rag.embeddings import generate_embedding
from rag.vectorstore import vector_search

def extract_exception_from_trace(error_text: str) -> str:
    """
    Extracts the exception, but ignores highly generic ones to force 
    the system into semantic vector search instead of strict filtering.
    """
    if not error_text: return None

    GENERIC_EXCEPTIONS = {
        "IllegalArgumentException",
        "NullPointerException",
        "RuntimeException",
        "IllegalStateException",
        "ApplicationContextException",
        "BeanCreationException",
    }
    
    pattern = r"\b(?:[a-zA-Z0-9_]+\.)*([A-Z][a-zA-Z0-9_]*(?:Exception|Error))\b"
    matches = re.findall(pattern, error_text)
    
    matches = [m for m in matches if len(m) > 6]
    
    if not matches:
        return None
        
    primary_exception = matches[0]
    
    # --- The Adaptive Logic ---
    if primary_exception in GENERIC_EXCEPTIONS:
        print(f"⚠️ Exception '{primary_exception}' is too generic. Bypassing strict filter for pure Semantic Search.")
        return None 
        
    return primary_exception

def summarize_error_for_search(error_text: str) -> str:
    """
    Uses an LLM to turn a messy stack trace into a clean 1-sentence 
    technical summary for better vector retrieval.
    """

    from llm.generator import generate_fix 
    
    prompt = f"""
    Analyze the following Java stack trace and output ONLY a 1-sentence technical 
    summary of the root cause. Focus on the specific Spring/Hibernate mechanism 
    failing (e.g., 'LazyInitializationException in Controller' or 'Circular Dependency').
    
    Error: {error_text[:2000]} # Limit text to avoid token waste
    """
    
    summary = generate_fix(prompt)
    return summary.strip() 

def retrieve_context(error_text: str, env_data: dict = None): 
    
    target_exception = extract_exception_from_trace(error_text)
    search_query = summarize_error_for_search(error_text)
    error_embedding = generate_embedding(search_query) 

    major_version = None
    if env_data and env_data.get("spring_boot_version") not in [None, "Unknown"]:
        major_version = env_data["spring_boot_version"].split(".")[0]
        print(f"🎯 Filtering RAG context for Spring Boot Major Version: {major_version}")

    final_results = []

    # --- SEARCH 1: Get the exact bug fixes (Top 3) ---
    bug_fixes = vector_search(
        embedding=error_embedding,
        exception_type=target_exception,
        top_k=4,
        major_version=major_version
    )
    
    # Fallback if no exact exception matches
    if not bug_fixes and target_exception:
        bug_fixes = vector_search(
            embedding=error_embedding,
            exception_type=None, 
            top_k=4,
            major_version=major_version
        )
    
    final_results.extend(bug_fixes)

    # --- SEARCH 2: Force fetch Official Docs ---
    official_docs = vector_search(
        embedding=error_embedding,
        exception_type=None,
        source_filter=['official_docs', 'spring-boot-guide', 'spring-boot-project', 'spring-boot-blog', 'github_wiki'], 
        top_k=1,
        min_score=0.4,
        major_version=major_version 
    )

    final_results.extend(official_docs)

    return final_results