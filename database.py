import mysql.connector
from config import db_config

# Maak verbinding met de database en retourneer de verbinding
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Zoek een kenteken in de database
def find_kenteken_in_db(kenteken):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kentekens WHERE kenteken = %s", (kenteken,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

# Voeg een nieuw kenteken toe aan de database
def add_kenteken_to_db(kenteken, merk, kleur):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO kentekens (kenteken, merk, kleur) VALUES (%s, %s, %s)",
        (kenteken, merk, kleur)
    )
    connection.commit()
    cursor.close()
    connection.close()

# Haal alle auto's op uit de database
def get_all_autos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kentekens")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# Update de gegevens van een bestaande auto in de database
def update_auto_in_db(kenteken, merk, kleur):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE kentekens SET merk = %s, kleur = %s WHERE kenteken = %s",
        (merk, kleur, kenteken)
    )
    connection.commit()
    cursor.close()
    connection.close()

# Verwijder een auto uit de database op basis van het kenteken
def delete_auto_from_db(kenteken):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM kentekens WHERE kenteken = %s", (kenteken,))
    connection.commit()
    cursor.close()
    connection.close()
