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

    query = """
        SELECT id, source, title, content,
               1 - (embedding <=> %s::vector) AS score
        FROM knowledge_base
        ORDER BY embedding <-> %s::vector
        LIMIT %s;
    """

    cur.execute(query, (embedding, embedding, top_k))
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
            "score": float(r[4])
        })

    return results
