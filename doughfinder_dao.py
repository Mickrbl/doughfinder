import psycopg2.extras
from db import get_db_connection


# ----------------------------
# LETTURA RACCOLTE
# ----------------------------

def get_raccolta_all():
    """
    Tutte le raccolte (aperte + chiuse), con username e num_donazioni.
    """
    query = """
        SELECT
            rf.*,
            u.id        AS utente_id,
            u.username  AS username,
            u.email     AS email,
            u.nome      AS nome,
            u.cognome   AS cognome,
            COALESCE(COUNT(d.id), 0) AS num_donazioni
        FROM raccolta_fondi rf
        LEFT JOIN utenti u ON rf.id_utente = u.id
        LEFT JOIN donazioni d ON d.id_rf = rf.id
        GROUP BY rf.id, u.id
        ORDER BY rf.scadenza ASC
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def get_raccolta():
    """
    Raccolte aperte (stato=0), con username e num_donazioni.
    """
    query = """
        SELECT
            rf.*,
            u.id        AS utente_id,
            u.username  AS username,
            u.email     AS email,
            u.nome      AS nome,
            u.cognome   AS cognome,
            COALESCE(COUNT(d.id), 0) AS num_donazioni
        FROM raccolta_fondi rf
        LEFT JOIN utenti u ON rf.id_utente = u.id
        LEFT JOIN donazioni d ON d.id_rf = rf.id
        WHERE rf.stato = 0
        GROUP BY rf.id, u.id
        ORDER BY rf.scadenza ASC
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def get_archivio():
    """
    Raccolte chiuse (stato=1). Qui non ti serve il count per forza,
    ma lo metto comunque così hai coerenza con i template se vuoi usarlo.
    """
    query = """
        SELECT
            rf.*,
            u.id        AS utente_id,
            u.username  AS username,
            u.email     AS email,
            u.nome      AS nome,
            u.cognome   AS cognome,
            COALESCE(COUNT(d.id), 0) AS num_donazioni
        FROM raccolta_fondi rf
        LEFT JOIN utenti u ON rf.id_utente = u.id
        LEFT JOIN donazioni d ON d.id_rf = rf.id
        WHERE rf.stato = 1
        GROUP BY rf.id, u.id
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def get_raccolta_singolo(id_rf):
    """
    Singola raccolta per pagina dettaglio.
    Serve username (come rf.username) per il template rf_singolo.html/paginarf.html
    """
    query = """
        SELECT
            rf.*,
            u.id        AS utente_id,
            u.username  AS username,
            u.email     AS email,
            u.nome      AS nome,
            u.cognome   AS cognome
        FROM raccolta_fondi rf
        LEFT JOIN utenti u ON rf.id_utente = u.id
        WHERE rf.id = %s
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query, (id_rf,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


# ----------------------------
# SCRITTURA RACCOLTE
# ----------------------------

def add_rf(rf, current, id_u, tipo, imgp, scadenza):
    query = """
        INSERT INTO raccolta_fondi
        (id_utente, titolo, descrizione, img, obiettivo, tipo, max_donazione, min_donazione, data, scadenza)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    conn = get_db_connection()
    cur = conn.cursor()
    success = False

    try:
        cur.execute(query, (
            id_u,
            rf['titolo'],
            rf['descrizione'],
            imgp,
            rf['obiettivo'],
            tipo,
            rf['max_donazione'],
            rf['min_donazione'],
            current,
            scadenza
        ))
        conn.commit()
        success = True
    except Exception as e:
        print("Error add_rf:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

    return success


def delete_rf(rf_id):
    query = "DELETE FROM raccolta_fondi WHERE id = %s"
    return _simple_update(query, (rf_id,))


def change_title(id_rf, new_title):
    query = "UPDATE raccolta_fondi SET titolo = %s WHERE id = %s"
    return _simple_update(query, (new_title, id_rf))


def change_description(id_rf, new_descrizione):
    query = "UPDATE raccolta_fondi SET descrizione = %s WHERE id = %s"
    return _simple_update(query, (new_descrizione, id_rf))


def change_scadenza(id_rf, new_scadenza):
    query = "UPDATE raccolta_fondi SET scadenza = %s WHERE id = %s"
    return _simple_update(query, (new_scadenza, id_rf))


def change_tipo(id_rf, new_tipo, new_scadenza):
    query = "UPDATE raccolta_fondi SET tipo = %s, scadenza = %s WHERE id = %s"
    return _simple_update(query, (new_tipo, new_scadenza, id_rf))


def change_goal(id_rf, new_goal):
    query = "UPDATE raccolta_fondi SET obiettivo = %s WHERE id = %s"
    return _simple_update(query, (new_goal, id_rf))


def change_minmax(id_rf, new_min, new_max):
    query = "UPDATE raccolta_fondi SET min_donazione=%s, max_donazione=%s WHERE id=%s"
    return _simple_update(query, (new_min, new_max, id_rf))


def change_img(id_rf, new_pic):
    query = "UPDATE raccolta_fondi SET img = %s WHERE id = %s"
    return _simple_update(query, (new_pic, id_rf))


def change_stato(id_rf):
    query = "UPDATE raccolta_fondi SET stato = 1 WHERE id = %s"
    return _simple_update(query, (id_rf,))


def success_rf(id_rf):
    query = "UPDATE raccolta_fondi SET successo = 1 WHERE id = %s"
    return _simple_update(query, (id_rf,))


# ----------------------------
# Helper interno
# ----------------------------

def _simple_update(query, params):
    conn = get_db_connection()
    cur = conn.cursor()
    success = False
    try:
        cur.execute(query, params)
        conn.commit()
        success = True
    except Exception as e:
        print("Error _simple_update:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return success
