import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag.embeddings import generate_embedding
from vectorstore import vector_search

query = input("Enter query: ")

emb = generate_embedding(query)
results = vector_search(emb, top_k=5)

print("\n=== RESULTS ===")
for r in results:
    print(f"[{r['source']}] {r['title']} (score={r['score']})")
    print(r["content"][:300], "...\n")
