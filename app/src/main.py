#!/usr/bin/env python3
from fastapi import FastAPI
from pydantic import BaseModel
from cipher import AESEncrypt, AESDecrypt
from db import dbHelper
import typing
import secrets

app = FastAPI()

storage = {}
storage = dbHelper()

def store_secret(secret: str, passphrase: typing.Optional[str]) -> str:
    """Store secret protected with passphrase and returns it's key"""
    key = secrets.token_urlsafe(64)

    # if passphrase is None, make it default
    passphrase = str(passphrase)
    encripted, iv = AESEncrypt(secret, passphrase)
    storage.insert(key, encripted, iv)

    return key


def get_secret(key: str, passphrase: typing.Optional[str]) -> typing.Optional[str]:
    """Returns secret by key or none if passphrase or key is incorrect"""

    # if passphrase is None, make it default
    passphrase = str(passphrase)

    document = storage.find(key)
    if document is None:
        # Wrong key
        return None

    encripted, iv = document

    message = AESDecrypt(encripted, passphrase, iv)
    if message is None:
        # Wrong passphrase
        return None

    storage.remove(key)
    return message


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
