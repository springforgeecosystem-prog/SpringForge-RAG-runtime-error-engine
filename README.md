# SpringForge RAG Runtime Error Engine

An AI-powered runtime error analysis and debugging assistant for Spring Boot applications. SpringForge uses Retrieval-Augmented Generation (RAG) to analyze stack traces, retrieve relevant documentation and solutions, and generate actionable fixes for Spring Boot runtime errors.

## 🎯 Overview

SpringForge combines:
- **Vector similarity search** to find relevant solutions from a knowledge base of Spring Boot documentation and Stack Overflow solutions
- **AWS Bedrock (Claude Sonnet 4)** for intelligent error analysis and fix generation
- **PostgreSQL with pgvector** for efficient semantic search
- **Flask REST API** for easy integration with IDEs and development tools

## ✨ Features

- 🔍 **Intelligent Error Analysis**: Automatically extracts root causes from complex stack traces
- 📚 **RAG-Enhanced Retrieval**: Searches a curated knowledge base of Spring Boot solutions and documentation
- 🤖 **LLM-Powered Fix Generation**: Generates context-aware, actionable fixes using Claude Sonnet 4
- 🎯 **Context-Aware Solutions**: Analyzes project file context alongside error traces
- 🔗 **Source Attribution**: Returns relevant documentation links and Stack Overflow references
- ⚡ **Fast Vector Search**: Leverages pgvector for efficient semantic similarity search

## 🏗️ Architecture

```
┌─────────────────┐
│   Client/IDE    │
└────────┬────────┘
         │ POST /analyze-error
         ▼
┌─────────────────┐
│   Flask API     │
│   (app.py)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  LLM Pipeline   │─────▶│   Prompt Builder │
│  (pipeline.py)  │      │(prompt_builder.py│
└────────┬────────┘      └──────────────────┘
         │                         │
         ▼                         ▼
┌─────────────────┐      ┌──────────────────┐
│  RAG Retriever  │◀────▶│  Vector Search   │
│ (retriever.py)  │      │(vectorstore.py)  │
└────────┬────────┘      └──────────────────┘
         │                         │
         │                         ▼
         │              ┌──────────────────┐
         │              │ PostgreSQL +     │
         │              │ pgvector         │
         │              │(Knowledge Base)  │
         │              └──────────────────┘
         ▼
┌─────────────────┐
│  AWS Bedrock    │
│ (Claude Sonnet) │
│  (generator.py) │
└─────────────────┘
```

## 📦 Installation

### Prerequisites

- Python 3.8+
- PostgreSQL with pgvector extension
- AWS Account with Bedrock access
- Environment variables configured

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SpringForge-RAG-runtime-error-engine
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # Database Configuration
   DB_HOST=your-db-host
   DB_PORT=5432
   DB_NAME=your-database-name
   DB_USER=your-username
   DB_PASSWORD=your-password
   PGVECTOR_URL=postgresql://user:pass@host:port/dbname
   
   # AWS Configuration (for Bedrock)
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_REGION=us-east-1
   ```

4. **Set up the knowledge base**
   
   Run the notebooks to ingest and embed documentation:
   ```bash
   jupyter notebook notebooks/rag_ingest_and_embeddings.ipynb
   ```

## 🚀 Usage

### Starting the Server

```bash
python app.py
```

The API server will start on `http://127.0.0.1:5000`

### API Endpoint

**POST** `/analyze-error`

**Request Body:**
```json
{
  "error": "java.lang.NullPointerException: Cannot invoke \"String.length()\" because \"str\" is null\n\tat com.example.demo.UserService.processUser(UserService.java:45)",
  "code_context": [
    {
      "path": "src/main/java/com/example/demo/UserService.java",
      "category": "service",
      "content": "public class UserService {\n  public void processUser(User user) {\n    String name = user.getName();\n    int length = name.length();\n  }\n}"
    }
  ]
}
```

**Response:**
```json
{
  "answer": "The error occurs because the 'name' variable is null. Add null check:\n\nif (name != null) {\n  int length = name.length();\n} else {\n  // Handle null case\n}",
  "retrieved_docs": [
    {
      "title": "How to handle NullPointerException in Spring Boot",
      "url": "https://stackoverflow.com/questions/..."
    }
  ]
}
```

### Testing

Use the provided test scripts:

```bash
# Test retrieval system
python scripts/test_retrieval.py

# Test fix generation
python scripts/test_fix_generation.py
```

Sample test payloads are available in `data/test-payloads/`:
- `NullPointerException.json`
- `LazyInitializationException.json`
- `circular_dependency.json`
- `StackOverflowError.json`
- And more...

## 📁 Project Structure

```
├── app.py                      # Flask API server
├── config.py                   # Configuration and environment variables
├── requirements.txt            # Python dependencies
│
├── llm/                        # LLM components
│   ├── bedrock_client.py       # AWS Bedrock integration
│   ├── generator.py            # Fix generation logic
│   ├── pipeline.py             # Main RAG pipeline orchestration
│   └── prompt_builder.py       # Prompt engineering
│
├── rag/                        # RAG components
│   ├── embeddings.py           # Embedding generation
│   ├── retriever.py            # Document retrieval with LLM summarization
│   └── vectorstore.py          # PostgreSQL/pgvector integration
│
├── data/                       # Knowledge base data
│   ├── merged_so_data.json     # Stack Overflow solutions
│   ├── normalized_dataset.json # Normalized knowledge entries
│   ├── springdocs.json         # Spring Boot documentation
│   ├── chunks/                 # Data chunks for ingestion
│   └── test-payloads/          # Sample error payloads for testing
│
├── notebooks/                  # Jupyter notebooks
│   ├── knowledge_db_data_so.ipynb       # Data processing
│   └── rag_ingest_and_embeddings.ipynb  # Vector embedding setup
│
└── scripts/                    # Testing scripts
    ├── test_fix_generation.py  # Test end-to-end fix generation
    └── test_retrieval.py       # Test retrieval accuracy
```

## 🛠️ Configuration

Key configuration parameters in [config.py](config.py):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `EMBED_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model for embeddings |
| `BEDROCK_MODEL_ID` | `us.anthropic.claude-3-7-sonnet-20250219-v1:0` | AWS Bedrock model |
| `MAX_TOKENS` | `800` | Maximum tokens for LLM response |
| `TEMPERATURE` | `0.2` | LLM temperature (lower = more focused) |
| `AWS_REGION` | `us-east-1` | AWS region for Bedrock |

## 🗄️ Knowledge Base

The system uses a PostgreSQL database with the pgvector extension to store:
- **Spring Boot official documentation** snippets
- **Stack Overflow solutions** for common runtime errors
- **Pre-computed embeddings** for fast similarity search

### Supported Error Types

- NullPointerException
- LazyInitializationException (Hibernate)
- Circular Dependency
- TransientPropertyValueException
- ObjectOptimisticLockingFailureException
- StackOverflowError
- Transaction rollback issues
- Silent failures
- And more...

## 🔧 How It Works

1. **Error Submission**: Client sends error trace and code context
2. **Error Summarization**: LLM extracts clean technical summary from stack trace
3. **Embedding Generation**: Summary is converted to vector embedding
4. **Vector Search**: Top-k similar documents retrieved from knowledge base
5. **Prompt Construction**: Error, code context, and retrieved docs combined into prompt
6. **Fix Generation**: Claude Sonnet analyzes and generates actionable fix
7. **Response**: Fix and source references returned to client

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Built with AWS Bedrock (Claude Sonnet 4)
- Uses sentence-transformers for embeddings
- Powered by PostgreSQL and pgvector
- Knowledge base sourced from Spring Boot documentation and Stack Overflow

---

**Note**: This is a research project for runtime error analysis and debugging assistance in Spring Boot applications.
