import os
import pandas as pd
import mysql.connector
from datetime import datetime
import json
from config import db_config


# Path to backup folder
backup_folder = 'C:/Users/bashi/Documents/kenteken_app/backups/'

def load_last_backup_time():
    """Load the timestamp of the last backup."""
    if os.path.exists('last_backup.json'):
        with open('last_backup.json', 'r') as f:
            data = json.load(f)
            return datetime.fromisoformat(data['last_backup'])
    return None

def update_last_backup_time(timestamp):
    """Update the timestamp of the last backup."""
    with open('last_backup.json', 'w') as f:
        json.dump({'last_backup': timestamp.isoformat()}, f)

def backup_database():
    """Function to backup the database."""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    last_backup = load_last_backup_time()
    query = "SELECT * FROM kentekens"
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        df = pd.DataFrame(rows)
        os.makedirs(backup_folder, exist_ok=True)
        csv_file = os.path.join(backup_folder, 'database_backup.csv')
        excel_file = os.path.join(backup_folder, 'database_backup.xlsx')

        df.to_csv(csv_file, index=False)
        df.to_excel(excel_file, index=False)

        print(f"Backup updated: {csv_file} and {excel_file}")
        update_last_backup_time(datetime.now())
    else:
        print("No new records added since the last backup.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    backup_database()

