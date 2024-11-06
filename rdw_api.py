import requests
from config import rdw_api_url

# Haal voertuiggegevens op van de RDW API
def get_vehicle_data_from_rdw(kenteken):
    # RDW API vereist kenteken zonder streepjes
    kenteken_api_format = kenteken.replace("-", "").upper()
    url = f"{rdw_api_url}{kenteken_api_format}"
    response = requests.get(url)

    # Controleer of we gegevens ontvangen van de RDW API
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return {
            'kenteken': kenteken,
            'merk': data.get('merk', 'Onbekend'),
            'kleur': data.get('eerste_kleur', 'Onbekend')
        }
    return None
