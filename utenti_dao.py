import psycopg2.extras
from db import get_db_connection

def get_user_by_id(id_utente):
    query = "SELECT * FROM utenti WHERE id = %s"
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query, (id_utente,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def get_utenti():
    query = "SELECT * FROM utenti"
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def esiste_email(email_utente):
    query = "SELECT 1 FROM utenti WHERE email = %s"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (email_utente,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

def create_user(nuovo_utente):
    query = """
        INSERT INTO utenti (email, username, password, nome, cognome, data_nascita)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    conn = get_db_connection()
    cur = conn.cursor()
    success = False
    try:
        cur.execute(query, (
            nuovo_utente["email"],
            nuovo_utente["username"],
            nuovo_utente["password"],
            nuovo_utente["nome"],
            nuovo_utente["cognome"],
            nuovo_utente["data_nascita"],
        ))
        conn.commit()
        success = True
    except Exception as e:
        print("Errore create_user:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return success

def get_user_by_email(email_utente):
    query = "SELECT * FROM utenti WHERE email = %s"
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query, (email_utente,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def change_password(email, new_password):
    query = "UPDATE utenti SET password = %s WHERE email = %s"
    return _simple_update(query, (new_password, email))

def success(id_utente, portafoglio):
    query = "UPDATE utenti SET portafoglio = %s WHERE id = %s"
    return _simple_update(query, (portafoglio, id_utente))

def _simple_update(query, params):
    conn = get_db_connection()
    cur = conn.cursor()
    success = False
    try:
        cur.execute(query, params)
        conn.commit()
        success = True
    except Exception as e:
        print("Errore update:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return success
