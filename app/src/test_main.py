from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_secrets_main():
    response = client.get("/secrets/")
    assert(response.status_code == 404)

    response = client.post("/generate", json={
        'secret': 'secret_1',
    })
    assert(response.status_code == 200)
    resp_json = response.json()
    assert('secret_key' in resp_json)

    secret_key = resp_json['secret_key']
    response = client.get('/secrets/{}'.format(secret_key))
    assert(response.status_code == 200)
    assert(response.json().get('secret', None) == 'secret_1')

    response = client.get('/secrets/{}'.format(secret_key))
    assert(response.status_code == 403)

def test_password_main():
    response = client.post("/generate", json={
        'secret': 'secret_2',
        'passphrase': 'pass_2',
    })
    assert(response.status_code == 200)
    resp_json = response.json()
    assert('secret_key' in resp_json)

    secret_key = resp_json['secret_key']
    response = client.get('/secrets/{}'.format(secret_key))
    assert(response.status_code == 403)
    response = client.get('/secrets/{}?passphrase={}'.format(secret_key, 'pass_2'))
    assert(response.status_code == 200)

