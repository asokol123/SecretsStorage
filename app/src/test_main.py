from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)

def test_secrets_main():
    response = client.get("/secrets/")
    assert(response.status_code == 404)

    secret = 'secret_1'

    response = client.post("/generate", json={
        'secret': secret,
    })
    assert(response.status_code == 200)
    resp_json = response.json()
    assert('secret_key' in resp_json)

    secret_key = resp_json['secret_key']
    response = client.get('/secrets/{}'.format(secret_key))
    assert(response.status_code == 200)
    assert(response.json().get('secret', None) == secret)

    response = client.get('/secrets/{}'.format(secret_key))
    assert(response.status_code == 403)

def test_password_main():
    secret = 'secret_2'
    passphrase = 'pass_2'
    response = client.post("/generate", json={
        'secret': secret,
        'passphrase': passphrase,
    })
    assert(response.status_code == 200)
    resp_json = response.json()
    assert('secret_key' in resp_json)

    secret_key = resp_json['secret_key']
    response = client.get('/secrets/{}'.format(secret_key))
    assert(response.status_code == 403)
    response = client.get('/secrets/{}?passphrase={}'.format(secret_key, passphrase))
    assert(response.status_code == 200)
    assert(response.json().get('secret', None) == secret)
    response = client.get('/secrets/{}?passphrase={}'.format(secret_key, passphrase))
    assert(response.status_code == 403)

def test_ttl_with_pass_main():
    secret = 'secret_3'
    passphrase = 'pass_3'
    response = client.post("/generate", json={
        'secret': secret,
        'passphrase': passphrase,
        'ttl': 3,
    })
    assert(response.status_code == 200)
    resp_json = response.json()
    assert('secret_key' in resp_json)

    time.sleep(5)
    secret_key = resp_json['secret_key']
    response = client.get('/secrets/{}?passphrase={}'.format(secret_key, passphrase))
    assert(response.status_code == 403)
    response = client.get('/secrets/{}?passphrase={}'.format(secret_key, passphrase))
    assert(response.status_code == 403)

    response = client.post("/generate", json={
        'secret': secret,
        'passphrase': passphrase,
        'ttl': 60,
    })
    assert(response.status_code == 200)
    resp_json = response.json()
    assert('secret_key' in resp_json)

    time.sleep(1)
    secret_key = resp_json['secret_key']
    response = client.get('/secrets/{}?passphrase={}'.format(secret_key, passphrase))
    assert(response.status_code == 200)
    assert(response.json().get('secret', None) == secret)
    response = client.get('/secrets/{}?passphrase={}'.format(secret_key, passphrase))
    assert(response.status_code == 403)

def test_only_ttl_main():
    secret = 'secret_4'
    response = client.post("/generate", json={
        'secret': secret,
        'ttl': 3,
    })
    assert(response.status_code == 200)
    resp_json = response.json()
    assert('secret_key' in resp_json)

    time.sleep(10)
    secret_key = resp_json['secret_key']
    response = client.get('/secrets/{}'.format(secret_key))
    assert(response.status_code == 403)

    response = client.post("/generate", json={
        'secret': secret,
        'ttl': 60,
    })
    assert(response.status_code == 200)
    resp_json = response.json()
    assert('secret_key' in resp_json)

    time.sleep(1)
    secret_key = resp_json['secret_key']
    response = client.get('/secrets/{}'.format(secret_key))
    assert(response.status_code == 200)
    assert(response.json().get('secret', None) == secret)
    response = client.get('/secrets/{}'.format(secret_key))
    assert(response.status_code == 403)
