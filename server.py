from fastapi import FastAPI, Query
import requests

app = FastAPI()

CBRF_API_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

def get_usd_rate() -> float:
    response = requests.get(CBRF_API_URL)
    data = response.json()
    return data['Valute']['USD']['Value']

@app.get('/convert')
def convert(rub_amount: str = Query(regex=r'^[0-9]+[,.][0-9]+$')):
    rub_amount = rub_amount.replace(',', '.')
    rub_amount = float(rub_amount)
    usd_rate = get_usd_rate()
    usd_amount = round(rub_amount / usd_rate, 2)
    return {'usd_amount': usd_amount}