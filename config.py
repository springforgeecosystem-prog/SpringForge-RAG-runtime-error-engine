import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")

EMBED_MODEL = "all-MiniLM-L6-v2"

# AWS
AWS_REGION = "us-east-1"

# Claude Sonnet 4
BEDROCK_MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"

# LLM params
MAX_TOKENS = 800
TEMPERATURE = 0.2

# DB
PGVECTOR_URL = os.getenv("PGVECTOR_URL")