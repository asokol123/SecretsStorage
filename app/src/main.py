#!/usr/bin/env python3
from cipher import Encrypt, Decrypt
from db import dbHelper
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import secrets
import typing

class InvalidSecretKey(Exception):
    pass

class InvalidPassphrase(Exception):
    pass

def get_mongo_addr(env):
    addr = env.get('MONGO_ADDR', None)
    if addr is None:
        return 'db'
    user = env.get('MONGO_USER', None)
    passwd = env.get('MONGO_PASS', None)
    if user and passwd:
        addr = 'mongodb://{}:{}@{}/'.format(user, passwd, addr)
    else:
        addr = 'mongodb://{}/'.format(addr)
    return addr

app = FastAPI()

storage = dbHelper(addr=get_mongo_addr(os.environ))
DEFAULT_PASSPHRASE = 'lorem_ipsum'

async def store_secret(secret: str, passphrase: typing.Optional[str], ttl: typing.Optional[int]) -> typing.Awaitable[str]:
    """Store secret protected with passphrase and returns it's key"""
    key = secrets.token_urlsafe(64)

    # if passphrase is None or empty, make it default
    if not passphrase:
        passphrase = DEFAULT_PASSPHRASE
    encripted, salt = Encrypt(secret, passphrase)
    await storage.insert(key, encripted, salt, ttl)

    return key


async def get_secret(key: str, passphrase: typing.Optional[str]) -> typing.Awaitable[typing.Optional[str]]:
    """Returns secret by key or none if passphrase or key is incorrect"""

    # if passphrase is None or empty, make it default
    if not passphrase:
        passphrase = DEFAULT_PASSPHRASE

    document = await storage.find(key)
    if document is None:
        raise InvalidSecretKey

    encripted, iv = document

    message = Decrypt(encripted, passphrase, iv)
    if message is None:
        raise InvalidPassphrase

    await storage.remove(key)
    return message


class ApiParamsGenerate(BaseModel):
    """Params of generate api method"""
    secret: str
    passphrase: typing.Optional[str] = None
    ttl: typing.Optional[int] = None

@app.post("/generate")
async def api_generate(params: ApiParamsGenerate):
    """Stores secret and returns secret key"""
    return {"secret_key": await store_secret(params.secret, params.passphrase, params.ttl)}


@app.get("/secrets/{secret_key}")
async def api_secrets(secret_key: str, passphrase: typing.Optional[str] = None):
    """Returns secret and deletes it"""
    # TODO: error message and status code if passphrase or secret_key is incorrect
    try:
        result = await get_secret(secret_key, passphrase)
        return JSONResponse(content={"secret": result})
    except InvalidPassphrase:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'Error': 'Invalid passphrase'})
    except InvalidSecretKey:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'Error': 'Invalid or expired secret key'})

