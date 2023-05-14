from fastapi import FastAPI, Query, HTTPException
from fastapi.openapi.utils import get_openapi
import requests
from requests.exceptions import RequestException

app = FastAPI()

CBRF_API_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

def get_usd_rate() -> float:
    try:
        response = requests.get(CBRF_API_URL)
        response.raise_for_status()
        data = response.json()
        return data['Valute']['USD']['Value']
    except RequestException:
        raise HTTPException(status_code=503, detail="Failed to get USD rate from CBRF API.")
    
def validate_rub_amount(rub_amount: str) -> float:
    try:
        rub_amount = rub_amount.replace(',', '.')
        return float(rub_amount)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid ruble amount format. Must be a number written with a dot or a comma (e.g. 100.50 or 100,50).")

@app.get(
    '/convert',
    summary='Converts RUB to USD.',
    description='Converts the specified amount of rubles to US dollars using the current exchange rate from CBRF.',
    tags=['currency']
)

def convert(
    rub_amount: str = Query(
        description="Amount of rubles to convert. Must be a non-integer number written with a dot or a comma.",
        regex=r'^[0-9]+[,.][0-9]+$',
        examples={
            "With dot": {"value": "100.00"},
            "With comma": {"value": "100,00"}
        }
    )
):
    rub_amount = validate_rub_amount(rub_amount)
    usd_rate = get_usd_rate()
    usd_amount = round(rub_amount / usd_rate, 2)
    return {'usd_amount': usd_amount}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Task API",
        version="1.0.2",
        description="This is a test-task API by Mikle",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi