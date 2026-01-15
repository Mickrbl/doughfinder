import os

database_url = os.environ.get("DATABASE_URL")

# Correzione comune per compatibilità
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Poi la usi nel connect
return psycopg2.connect(database_url, sslmode="require")