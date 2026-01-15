import psycopg2.extras
from db import get_db_connection

def count_donazioni_per_rf(id_rf: int) -> int:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM donazioni WHERE id_rf = %s", (id_rf,))
    n = cur.fetchone()[0]
    cur.close()
    conn.close()
    return n


def get_donazioni():
    query = """
        SELECT
            d.id,
            d.nome,
            d.cognome,
            d.donazione,
            d.id_rf,
            d.anonimo
        FROM donazioni d
        ORDER BY d.id DESC
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def add_donazione(donazione, id_rf, anonimo):
    query = '''
        INSERT INTO donazioni (nome, cognome, donazione, id_rf, anonimo)
        VALUES (%s, %s, %s, %s, %s)
    '''

    conn = get_db_connection()
    cur = conn.cursor()
    success = False

    try:
        cur.execute(query, (
            donazione['nome'],
            donazione['cognome'],
            donazione['donazione'],
            id_rf,
            anonimo
        ))
        conn.commit()
        success = True
    except Exception as e:
        print('Error:', e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

    return success
