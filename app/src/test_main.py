from fastapi.testclient import TestClient
from main import app
import time
import typing

client = TestClient(app)

def generate(secret: str, passphrase: typing.Optional[str]=None, ttl: typing.Optional[int]=None) -> str:
    params = {'secret': secret}
    if passphrase:
        params['passphrase'] = passphrase
    if ttl:
        params['ttl'] = ttl
    response = client.post("/generate", json=params)
    return response.json()['secret_key']


def get_secret(secret_key: str, passwd: typing.Optional[str] = None) -> typing.Tuple[int, typing.Optional[str]]:
    if passwd is None:
        response = client.get('/secrets/{}'.format(secret_key))
    else:
        response = client.get('/secrets/{}?passphrase={}'.format(secret_key, passwd))
    return response.status_code, response.json().get('secret', None)


def test_secrets_main():
    response = client.get("/secrets/")
    assert(response.status_code == 404)

    secret = 'secret_1'
    secret_code = generate(secret)

    status, ans = get_secret(secret_code)
    assert(status == 200)
    assert(ans == secret)

    status, ans = get_secret(secret_code)
    assert(status == 403)


def test_password_main():
    secret = 'secret_2'
    passphrase = 'pass_2'

    secret_key = generate(secret, passphrase=passphrase)
    status, ans = get_secret(secret_key)
    assert(status == 403)
    status, ans = get_secret(secret_key, gen_incorrect_pass(passphrase))
    assert(status == 403)
    status, ans = get_secret(secret_key, '')
    assert(status == 403)
    status, ans = get_secret(secret_key, passphrase)
    assert(status == 200)
    assert(ans == secret)
    status, ans = get_secret(secret_key)
    assert(status == 403)


def gen_incorrect_pass(passwd):
    assert(passwd)
    return passwd[:-1] + chr(ord(passwd[-1]) ^ 1)


def test_ttl_with_pass_main():
    secret = 'secret_3'
    passphrase = 'pass_3'

    secret_key = generate(secret, passphrase=passphrase, ttl=3)

    time.sleep(5)
    status, ans = get_secret(secret_key, passphrase)
    assert(status == 403)
    status, ans = get_secret(secret_key)
    assert(status == 403)

    secret_key = generate(secret, passphrase=passphrase, ttl=60)
    time.sleep(1)
    status, ans = get_secret(secret_key)
    assert(status == 403)
    status, ans = get_secret(secret_key, gen_incorrect_pass(passphrase))
    assert(status == 403)
    status, ans = get_secret(secret_key, '')
    assert(status == 403)
    status, ans = get_secret(secret_key, passphrase)
    assert(status == 200)
    assert(ans == secret)
    status, ans = get_secret(secret_key, passphrase)
    assert(status == 403)

def test_only_ttl_main():
    secret = 'secret_4'

    secret_key = generate(secret, ttl=3)

    time.sleep(5)
    status, ans = get_secret(secret_key)
    assert(status == 403)


    secret_key = generate(secret, ttl=60)

    time.sleep(5)
    status, ans = get_secret(secret_key)
    assert(status == 200)
    assert(ans == secret)
    status, ans = get_secret(secret_key)
    assert(status == 403)
