import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

url = "postgresql://postgres.nnrscmvqajfuasbenuxy:hrouSFyYvPdmvaUh@aws-0-us-east-1.pooler.supabase.com:5432/postgres"

print("Conectando ao Supabase...")
conn = psycopg2.connect(url)
cur = conn.cursor(cursor_factory=RealDictCursor)

cur.execute("SELECT to_regclass('public.rag_chunks') AS table_exists")
print("table_exists:", cur.fetchone())

cur.execute("SELECT COUNT(*) AS total FROM public.rag_chunks")
print("total_registros:", cur.fetchone())

cur.execute("SELECT * FROM public.rag_chunks LIMIT 10")
rows = cur.fetchall()
print(json.dumps([dict(r) for r in rows], ensure_ascii=False, default=str))

cur.close()
conn.close()
