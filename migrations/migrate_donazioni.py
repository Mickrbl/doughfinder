import sqlite3
from db import get_db_connection

sqlite = sqlite3.connect('db/db_doughfinder.db')
sqlite.row_factory = sqlite3.Row

pg = get_db_connection()
cur = pg.cursor()

rows = sqlite.execute("SELECT * FROM donazioni").fetchall()

for r in rows:
    cur.execute("""
        INSERT INTO donazioni (id, nome, cognome, donazione, id_rf, anonimo)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id) DO NOTHING
    """, (
        r['id'],
        r['nome'],
        r['Cognome'],   # <- colonna SQLite
        r['donazione'],
        r['id_rf'],
        r['anonimo']
    ))

pg.commit()
cur.close()
pg.close()
sqlite.close()

print("✅ Migrazione donazioni completata")
