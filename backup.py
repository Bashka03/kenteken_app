import os
import pandas as pd
import mysql.connector
from datetime import datetime
import json

# Configuratie voor databaseverbinding
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'kenteken_db'
}

# Pad waar de back-ups worden opgeslagen
backup_folder = 'C:/Users/bashi/Documents/kenteken_app/backups/'

# Laad de timestamp van de laatste back-up
def load_last_backup_time():
    if os.path.exists('last_backup.json'):
        with open('last_backup.json', 'r') as f:
            data = json.load(f)
            return datetime.fromisoformat(data['last_backup'])
    return None

# Update de timestamp van de laatste back-up
def update_last_backup_time(timestamp):
    with open('last_backup.json', 'w') as f:
        json.dump({'last_backup': timestamp.isoformat()}, f)

# Functie om de database te controleren en een back-up te maken
def backup_database():
    # Maak verbinding met de database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Timestamp van laatste back-up ophalen
    last_backup = load_last_backup_time()
    
    # Zoek naar nieuwe kentekens sinds de laatste back-up
    query = "SELECT * FROM kentekens"
    if last_backup:
        #query += " WHERE toegevoegd_op > %s"
        cursor.execute(query)
    else:
        cursor.execute(query)

    rows = cursor.fetchall()

    if rows:
        # Maak een DataFrame van de gegevens
        df = pd.DataFrame(rows)
        
        # Zorg dat de back-up map bestaat
        os.makedirs(backup_folder, exist_ok=True)
        
        # Bestandspaden voor de back-ups
        csv_file = os.path.join(backup_folder, 'database_backup.csv')
        excel_file = os.path.join(backup_folder, 'database_backup.xlsx')

        # Schrijf de back-up data naar hetzelfde .csv en .xlsx bestand
        df.to_csv(csv_file, index=False)
        df.to_excel(excel_file, index=False)

        print(f"Back-up geüpdatet: {csv_file} en {excel_file}")

        # Update laatste back-up tijd
        update_last_backup_time(datetime.now())
    else:
        print("Geen nieuwe kentekens toegevoegd sinds de laatste back-up.")


    # Sluit de databaseverbinding
    cursor.close()
    conn.close()

if __name__ == "__main__":
    backup_database()
