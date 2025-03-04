import requests
from datetime import datetime

# Configuración de la API
API_URL = "https://sim-swap.p-eu.rapidapi.com/sim-swap/sim-swap/v0/retrieve-date"
HEADERS = {
    "Content-Type": "application/json",
    "x-rapidapi-host": "sim-swap.nokia.rapidapi.com",
    "x-rapidapi-key": "3aa9d376cfmsh16446717213dd03p1e3dfdjsn0c3cc2207d6f"
}


# Función para consultar el cambio de SIM
def sim_change_chack(numero):
    payload = {"phoneNumber": numero}


    response = requests.post(API_URL, json=payload, headers=HEADERS)
    data = response.json()
    latest_change = data['latestSimChange']

    # Convert API timestamp to datetime object
    change_date = datetime.fromisoformat(latest_change.replace('Z', '+00:00'))

    # Get current time
    current_time = datetime.now(change_date.tzinfo)

    # Calculate time difference in days
    time_diff = current_time - change_date
    time_diff_days = time_diff.total_seconds() / (60 * 60 * 24)

    # Determine if change was recent (less than 1 day)
    is_recent = time_diff_days < 1

    return is_recent

