from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")

def generate_embedding(text: str):
    """
    Generates a 384-dimensional embedding vector from the given text using the SentenceTransformer model.

    Args:
        text (str): The input text to be embedded.

    Returns:
        List[float]: A list of 384 float values representing the embedding vector.
    """
    # Creates a 384-dim embedding vector from text.
    return model.encode(text).tolist()
