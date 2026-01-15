import os
import psycopg2

def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL non impostata")

    return psycopg2.connect(database_url, sslmode="require")
