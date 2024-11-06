from flask import Flask
from routes import app_routes
import threading
import time
from datetime import datetime
import sys
import os
import subprocess  # Om backup.py uit te voeren
from auth import auth



app = Flask(__name__)
app.secret_key = 'geheim'


# Register routes from routes.py
app.register_blueprint(app_routes)
app.register_blueprint(auth, url_prefix='/auth')  # Auth routes onder /auth

# Functie om backup.py handmatig en dagelijks om 11:00 uur uit te voeren
def start_daily_backup():
    # Volledige pad naar het backup.py script
    backup_script = os.path.join(os.path.dirname(__file__), 'backup.py')
    # Start de eerste back-up meteen bij het opstarten
    subprocess.run([sys.executable, backup_script])
    print("Back-up bij opstarten voltooid.")

    # Wacht tot dagelijks 11:00 voor de volgende back-up
    while True:
        now = datetime.now()
        if now.hour == 11 and now.minute == 00:  # Controleer of het 11:00 is
            subprocess.run([sys.executable, backup_script])
            print("Dagelijkse back-up om 11:00 voltooid.")
            time.sleep(60)  # Wacht een minuut om te voorkomen dat de back-up meerdere keren binnen het uur draait
        else:
            time.sleep(30)  # Controleer elke 30 seconden

# Start een thread voor de dagelijkse back-up functie
backup_thread = threading.Thread(target=start_daily_backup)
backup_thread.daemon = True  # Zorgt ervoor dat de thread stopt wanneer de main thread stopt
backup_thread.start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
