import mysql.connector
from config import db_config

def get_db_connection():
    return mysql.connector.connect(**db_config)

def find_kenteken_in_db(kenteken):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kentekens WHERE kenteken = %s", (kenteken,))
        result = cursor.fetchone()
    return result

def add_kenteken_to_db(kenteken, merk, kleur):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO kentekens (kenteken, merk, kleur) VALUES (%s, %s, %s)",
            (kenteken, merk, kleur)
        )
        conn.commit()

def get_all_autos():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kentekens")
        result = cursor.fetchall()
    return result

def update_auto_in_db(kenteken, merk, kleur):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE kentekens SET merk = %s, kleur = %s WHERE kenteken = %s",
            (merk, kleur, kenteken)
        )
        conn.commit()

def delete_auto_from_db(kenteken):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kentekens WHERE kenteken = %s", (kenteken,))
        conn.commit()

