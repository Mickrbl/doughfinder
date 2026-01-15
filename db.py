import psycopg2
import psycopg2.extras
import os


def get_db_connection():
    """
    Usa DATABASE_URL se presente (Railway/produzione),
    altrimenti fallback a parametri locali.
    """
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Railway usa DATABASE_URL tipo:
        # postgres://user:pass@host:port/dbname
        # psycopg2 accetta anche "postgres://"
        return psycopg2.connect(database_url)

    # fallback locale (se vuoi tenerlo)
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "doughfinder"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )
