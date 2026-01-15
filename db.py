import os
import psycopg2
from urllib.parse import urlparse

def get_db_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL non presente nelle env")

    # DEBUG sicuro: NON stampa la password, solo info utili + lunghezza password
    try:
        u = urlparse(database_url)
        pwd_len = len(u.password) if u.password else 0
        print(f"DB DEBUG host={u.hostname} port={u.port} db={u.path} user={u.username} pwd_len={pwd_len}")
    except Exception as e:
        print("DB DEBUG parse error:", e)

    return psycopg2.connect(database_url)
