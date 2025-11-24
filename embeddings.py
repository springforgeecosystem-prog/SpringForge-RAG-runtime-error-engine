from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str):

  # Creates a 384-dim embedding vector from text.

    return model.encode(text).tolist()
