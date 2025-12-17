from rag.retriever import retrieve_context
from rag.prompt_builder import build_prompt
from rag.generator import generate_fix

def run(error: str, code_context: list):
    retrieved_docs = retrieve_context(error)

    prompt = build_prompt(
        error=error,
        code_context=code_context,
        retrieved_docs=retrieved_docs
    )

    answer = generate_fix(prompt)

    return {
        "answer": answer,
        "retrieved_docs": retrieved_docs
    }
