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

def vector_search(embedding, exception_type=None, source_filter=None, major_version=None, top_k=5, min_score=0.50):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT id, source, title, content, url,
               1 - (embedding <=> %(emb)s::vector) AS score,
               metadata->>'spring_version' AS doc_version 
        FROM knowledge_base
        WHERE 1=1
    """
    params = {"emb": embedding, "limit": top_k}

    if exception_type:
        query += " AND metadata->>'exception_type' = %(exc)s"
        params["exc"] = exception_type

    if source_filter:
        query += " AND source = ANY(%(sources)s)"
        params["sources"] = list(source_filter) 

    if major_version:
        query += """
            AND (
                metadata->>'spring_version' LIKE %(v_dot)s
                OR metadata->>'spring_version' LIKE %(v_x)s
                OR metadata->>'spring_version' IS NULL
            )
        """
        params["v_dot"] = f"{major_version}.%" 
        params["v_x"] = f"{major_version}.x"   

    query += """
        ORDER BY embedding <=> %(emb)s::vector 
        LIMIT %(limit)s;
    """

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = []
    for r in rows:
        score = float(r[5])
        doc_version = r[6]
        
        if min_score is None or score >= min_score:
            results.append({
                "id": r[0], "source": r[1], "title": r[2], 
                "content": r[3], "url": r[4], "score": score, 
                "spring_version": doc_version 
            })
        else:
            print(f"🗑️ Dropped noisy doc: '{r[2]}' (Score: {score:.2f} is below {min_score})")

    return results