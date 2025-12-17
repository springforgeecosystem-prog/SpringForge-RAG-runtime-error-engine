def build_prompt(error: str, code_context: list, retrieved_docs: list) -> str:
    prompt = f"""
You are an expert Spring Boot debugging assistant.

A runtime error occurred in a Spring Boot application.

--- ERROR TRACE ---
{error}

--- PROJECT FILE CONTEXT ---
"""

    for file in code_context:
        prompt += f"""
File: {file['path']}
Category: {file.get('category')}
Content:
{file['content']}
"""

    prompt += "\n--- RELEVANT KNOWLEDGE BASE DOCUMENTS ---\n"

    for doc in retrieved_docs:
        prompt += f"""
Source: {doc.get('source', 'unknown')}
Content:
{doc.get('content')}
"""

    prompt += """
--- TASK ---
1. Identify the root cause
2. Explain why it happened
3. Suggest a concrete fix
4. Show corrected code snippets if applicable
"""

    return prompt
