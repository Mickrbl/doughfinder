import sqlite3
from db import get_db_connection

sqlite = sqlite3.connect('db/db_doughfinder.db')
sqlite.row_factory = sqlite3.Row

pg = get_db_connection()
cur = pg.cursor()

rows = sqlite.execute("SELECT * FROM raccolta_fondi").fetchall()

for r in rows:
    cur.execute("""
        INSERT INTO raccolta_fondi
        (id, id_utente, titolo, descrizione, img, obiettivo, tipo, max_donazione, min_donazione,
         data, "like", stato, donazioni, scadenza, successo)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id) DO NOTHING
    """, (
        r['id'], r['id_utente'], r['titolo'], r['descrizione'], r['img'],
        r['obiettivo'], r['tipo'], r['max_donazione'], r['min_donazione'],
        r['data'], r['like'], r['stato'], r['donazioni'], r['scadenza'], r['successo']
    ))

pg.commit()
cur.close()
pg.close()
sqlite.close()

print("✅ Migrazione raccolta_fondi completata")
