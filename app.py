from flask import Flask, request, render_template, redirect, url_for, jsonify
import mysql.connector
import requests

app = Flask(__name__)


# Configuratie voor MySQL-verbinding
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'kenteken_db'
}

# Database-verbinding
def get_db_connection():
    return mysql.connector.connect(**db_config)
# Functie om RDW API aan te roepen (zonder streepjes, omdat de RDW API alleen kentekens zonder streepjes accepteert)
def get_vehicle_data_from_rdw(kenteken):
    kenteken_api_format = kenteken.replace("-", "").upper()
    url = f"https://opendata.rdw.nl/resource/m9d7-ebf2.json?kenteken={kenteken_api_format}"
    response = requests.get(url)
    
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        # Alleen de benodigde gegevens selecteren
        return {
            'kenteken': kenteken,
            'merk': data.get('merk', 'Onbekend'),
            'kleur': data.get('eerste_kleur', 'Onbekend')
        }
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_kenteken', methods=['POST'])
def check_kenteken():
    kenteken = request.form.get('kenteken').upper()

    if not kenteken:
        return jsonify({'error': 'Voer een kenteken in'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Controleer of kenteken al in de database bestaat
    cursor.execute("SELECT * FROM kentekens WHERE kenteken = %s", (kenteken,))
    result = cursor.fetchone()

    if result:
        # Kenteken gevonden in database, toon de gegevens
        cursor.close()
        connection.close()
        return render_template('result.html', kenteken_data=result, gevonden=True)
    else:
        # Kenteken niet gevonden, haal gegevens op van de RDW API
        vehicle_data = get_vehicle_data_from_rdw(kenteken)
        if vehicle_data:
            try:
                # Voeg kenteken, merk en kleur toe aan de database, inclusief streepjes in het kenteken
                cursor.execute(
                    "INSERT INTO kentekens (kenteken, merk, kleur) VALUES (%s, %s, %s)",
                    (vehicle_data['kenteken'], vehicle_data['merk'], vehicle_data['kleur'])
                )
                connection.commit()
                cursor.close()
                connection.close()
                # Toon de nieuw geregistreerde gegevens
                return render_template('result.html', kenteken_data=vehicle_data, gevonden=True)
            except mysql.connector.Error as err:
                cursor.close()
                connection.close()
                return jsonify({'error': str(err)}), 500
        else:
            # Geen gegevens gevonden bij RDW, toon een foutmelding
            cursor.close()
            connection.close()
            return render_template('result.html', kenteken_data={'kenteken': kenteken}, gevonden=False, fout="Kenteken niet gevonden bij RDW")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)