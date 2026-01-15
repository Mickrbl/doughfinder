import sqlite3
from db import get_db_connection

sqlite = sqlite3.connect('db/db_doughfinder.db')
sqlite.row_factory = sqlite3.Row

pg = get_db_connection()
cur = pg.cursor()

rows = sqlite.execute("SELECT * FROM utenti").fetchall()

for r in rows:
    cur.execute("""
        INSERT INTO utenti (id, nome, cognome, username, email, password, data_nascita, portafoglio)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id) DO NOTHING
    """, (
        r['id'], r['nome'], r['cognome'], r['username'], r['email'],
        r['password'], r['data_nascita'], r['portafoglio']
    ))

pg.commit()
cur.close()
pg.close()
sqlite.close()

print("✅ Migrazione utenti completata")
