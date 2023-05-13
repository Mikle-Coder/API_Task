import requests

SERVER_URL = 'http://localhost:8000'

def convert_currency(rub_amount: str) -> float:
    response = requests.get(SERVER_URL + '/convert', params={'rub_amount': rub_amount})
    data = response.json()
    return data['usd_amount']