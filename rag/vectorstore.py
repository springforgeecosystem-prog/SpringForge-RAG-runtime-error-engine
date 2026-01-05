import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

def get_connection():

    #Connect to Supabase Postgres
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        sslmode="require"
    )

def vector_search(embedding, top_k=5):
    conn = get_connection()
    cur = conn.cursor()

    # Use %(name)s for named parameters - cleaner and no IndexError
    query = """
        SELECT id, source, title, content, url,
               1 - (embedding <=> %(emb)s::vector) AS score
        FROM knowledge_base
        ORDER BY embedding <-> %(emb)s::vector
        LIMIT %(limit)s;
    """

    cur.execute(query, {
        "emb": embedding, 
        "limit": top_k
    })
    
    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "source": r[1],
            "title": r[2],
            "content": r[3],
            "url": r[4],
            "score": float(r[5]),
        })

    return results
