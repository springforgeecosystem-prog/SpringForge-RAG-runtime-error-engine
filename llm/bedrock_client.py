import boto3
import json
from config import (
    AWS_REGION,
    BEDROCK_MODEL_ID,
    MAX_TOKENS,
    TEMPERATURE
)

class BedrockClient:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION
        )

    def generate(self, prompt: str) -> str:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }

        response = self.client.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(body)
        )

        response_body = json.loads(response["body"].read())

        return response_body["content"][0]["text"]
