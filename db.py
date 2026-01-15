import psycopg2
import psycopg2.extras

def get_db_connection():
    return psycopg2.connect(dbname="doughfinder")
