from llm.bedrock_client import BedrockClient

llm = BedrockClient()

def generate_fix(prompt: str) -> str:
    return llm.generate(prompt)