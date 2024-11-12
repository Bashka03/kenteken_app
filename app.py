from flask import Flask
from routes import app_routes
from auth import auth
import threading
import time
import os
import subprocess
from datetime import datetime
import sys

app = Flask(__name__)
app.secret_key = 'geheim'

# Register routes from different modules
app.register_blueprint(app_routes)
app.register_blueprint(auth, url_prefix='/auth')

def execute_backup_script():
    """Execute the backup script located at the root directory."""
    backup_script = os.path.join(os.path.dirname(__file__), 'backup.py')
    subprocess.run([sys.executable, backup_script])
    print("Backup executed.")

def start_daily_backup():
    """Run the backup script daily at 11:00 AM."""
    execute_backup_script()

    while True:
        now = datetime.now()
        if now.hour == 11 and now.minute == 0:  # 11:00 AM check
            execute_backup_script()
            print("Daily backup completed at 11:00 AM.")
            time.sleep(60)  # Prevent multiple executions
        else:
            time.sleep(30)  # Check again

# Start a thread for the backup
backup_thread = threading.Thread(target=start_daily_backup)
backup_thread.daemon = True
backup_thread.start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)

