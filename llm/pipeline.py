from rag.retriever import retrieve_context
from llm.prompt_builder import build_prompt
from llm.generator import generate_fix

def run(error: str, code_context: list):
    retrieved_docs = retrieve_context(error)

    prompt = build_prompt(
        error=error,
        code_context=code_context,
        retrieved_docs=retrieved_docs
    )

    answer = generate_fix(prompt)

    clean_docs = [
        {
            "title": doc["title"],
            "url": doc["url"]
        }
        for doc in retrieved_docs
    ]

    return {
        "answer": answer,
        "retrieved_docs": clean_docs
    }
