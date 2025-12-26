"""
example.py

Template for config.py. 
Rename to config.py and fill in your actual values locally.
Do NOT commit real secrets to GitHub.
"""

# Database
DB_HOST = "your_db_host_here"
DB_PORT = 5432  # example port
DB_NAME = "your_db_name_here"
DB_USER = "your_db_user_here"
DB_PASS = "your_db_password_here"

# Embedding model
EMBED_MODEL = "all-MiniLM-L6-v2"

# AWS
AWS_REGION = "your_aws_region_here"

# Claude Sonnet 4
BEDROCK_MODEL_ID = "your_bedrock_model_id_here"

# LLM parameters
MAX_TOKENS = 800
TEMPERATURE = 0.2

# PGVector
PGVECTOR_URL = "your_pgvector_url_here"
