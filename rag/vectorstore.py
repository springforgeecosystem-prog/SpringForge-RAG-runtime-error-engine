import psycopg2
import time
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

def get_connection(use_direct=False, retry_count=3):
    """
    Connect to Supabase Postgres with retry logic
    
    Args:
        use_direct: If True, use direct connection (db.region.supabase.co:5432)
                   If False, use pooler (pooler.region.supabase.co:6543)
        retry_count: Number of retries on failure
    """
    host = DB_HOST
    port = DB_PORT
    
    # If pooler is failing, try direct connection instead
    if use_direct and "pooler" in host:
        host = host.replace("pooler.", "db.")
        port = 5432
        print(f"[Switching to direct connection: {host}:{port}]")
    
    for attempt in range(retry_count):
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                sslmode="require",
                connect_timeout=10
            )
            print(f"✓ Connected to {host}:{port}")
            return conn
        except psycopg2.OperationalError as e:
            error_msg = str(e).lower()
            if attempt < retry_count - 1:
                wait_time = 2 ** attempt
                print(f"⚠ Connection failed (attempt {attempt + 1}/{retry_count}): {str(e)[:80]}")
                print(f"  Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                if not use_direct and "pooler" in DB_HOST:
                    print(f"\n⚠ Pooler connection failed. Switching to direct connection...")
                    return get_connection(use_direct=True, retry_count=1)
                else:
                    raise

def vector_search(embedding, exception_type=None, source_filter=None, major_version=None, top_k=5, min_score=0.50):
    """Vector search with automatic fallback to direct connection if pooler fails"""
    try:
        conn = get_connection(use_direct=False)
    except psycopg2.OperationalError as e:
        # If pooler fails, automatically try direct connection
        print(f"\n⚠ Pooler connection failed, trying direct connection...")
        conn = get_connection(use_direct=True)
    
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

    try:
        cur.execute(query, params)
        rows = cur.fetchall()
    finally:
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


def hybrid_search(query_text, embedding, top_k=5, **kwargs):
    """
    Hybrid search combining keyword and semantic search
    This is an alias for vector_search with the same parameters
    """
    return vector_search(embedding=embedding, top_k=top_k, **kwargs)