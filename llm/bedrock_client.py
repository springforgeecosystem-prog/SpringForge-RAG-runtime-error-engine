import boto3
import json
import time
from botocore.exceptions import ClientError
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
        self.last_request_time = 0
        self.min_delay = 2.0 

    def generate(self, prompt: str) -> str:
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last
            print(f"⏱️ Rate limiting: waiting {sleep_time:.1f}s...")
            time.sleep(sleep_time)

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

        # Retry logic with exponential backoff
        max_retries = 3
        base_delay = 5
        
        for attempt in range(max_retries):
            try:
                self.last_request_time = time.time()
                
                response = self.client.invoke_model(
                    modelId=BEDROCK_MODEL_ID,
                    body=json.dumps(body)
                )

                response_body = json.loads(response["body"].read())
                return response_body["content"][0]["text"]
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                
                if error_code == 'ThrottlingException':
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt) 
                        print(f"Throttled! Waiting {delay}s before retry {attempt + 1}/{max_retries}...")
                        time.sleep(delay)
                        continue
                    else:
                        raise Exception(f"Max retries exceeded due to throttling. Try running with --max-cases 1 or wait 5 minutes.")
                else:
                    raise e
            except Exception as e:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"Error occurred, retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    raise e
        
        raise Exception("Failed after all retries")
