from fastapi import FastAPI
from pydantic import BaseModel
import typing
import secrets

app = FastAPI()

# TODO: replace with DB
storage = {}

def store_secret(secret: str, passphrase: typing.Optional[str]) -> str:
    """Store secret protected with passphrase and returns it's key"""
    # TODO: replace with DB
    key = secrets.token_urlsafe(64)

    # TODO: replace with hash
    storage[key] = (secret, passphrase)
    return key


def get_secret(key: str, passphrase: typing.Optional[str]) -> typing.Optional[str]:
    """Returns secret by key or none if passphrase or key is incorrect"""
    if key not in storage:
        # Wrong key
        return None
    secret, secret_pass = storage[key]
    if secret_pass is not None and secret_pass != passphrase:
        # Wrong passphrase
        return None
    storage.pop(key)
    return secret


class ApiParamsGenerate(BaseModel):
    """Params of generate api method"""
    secret: str
    passphrase: typing.Optional[str] = None

@app.post("/generate")
def api_generate(params: ApiParamsGenerate):
    """Stores secret and returns secret key"""
    return {"secret_key": store_secret(params.secret, params.passphrase)}


@app.get("/secrets/{secret_key}")
def api_secrets(secret_key: str, passphrase: typing.Optional[str] = None):
    """Returns secret and deletes it"""
    # TODO: error message and status code if passphrase or secret_key is incorrect
    return {"secret": get_secret(secret_key, passphrase)}
