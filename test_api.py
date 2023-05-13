import pytest
from fastapi.testclient import TestClient
from server import app, get_usd_rate
from client import convert_currency, SERVER_URL

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_get_usd_rate():
    usd_rate = get_usd_rate()
    assert isinstance(usd_rate, float)
    assert usd_rate > 0 and usd_rate < 150

def test_convert_currency_invalid_input(client):
    expected_json = {"detail":[{"loc":["query","rub_amount"],"msg":"string does not match regex \"^[0-9]+[,.][0-9]+$\"","type":"value_error.str.regex","ctx":{"pattern":"^[0-9]+[,.][0-9]+$"}}]}
    expected_status_code = 422
    amounts = ['abc', '100', '']
    for amount in amounts:
        response = client.get(f"{SERVER_URL}/convert?rub_amount={amount}")
        assert response.status_code == expected_status_code
        assert response.json() == expected_json

def test_convert_currency_currect_input(client):
    expected_status_code = 200
    amounts = ['123.45', '123,45']
    for amount in amounts:
        response = client.get(f"{SERVER_URL}/convert?rub_amount={amount}")
        assert response.status_code == expected_status_code
        assert 'usd_amount' in response.json().keys()

def test_client_convert_currency():
    usd_amount = convert_currency('100.0')
    assert isinstance(usd_amount, float)