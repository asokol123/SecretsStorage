[![Build Status](https://travis-ci.com/asokol123/SecretsStorage.svg?branch=master)](https://travis-ci.com/asokol123/SecretsStorage) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/08b2907c55dc4d80aac4823b6f924f42)](https://www.codacy.com/manual/asokol123/SecretsStorage?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=asokol123/SecretsStorage&amp;utm_campaign=Badge_Coverage) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/08b2907c55dc4d80aac4823b6f924f42)](https://www.codacy.com/manual/asokol123/SecretsStorage?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=asokol123/SecretsStorage&amp;utm_campaign=Badge_Grade)

# SecretsStorage

Secrets storage with fastAPI

## General
This is similar to <https://onetimesecret.com/>, but JsonAPI only.
You can:
*   Create note, optionally protect it with psasphrase and set timeout
*   Get note. After getting it will be deleted.

## API
There is swagger UI in /docs and redoc in /redoc

## Building
You need docker-compose to use this app.
```bash
git clone https://github.com/asokol123/SecretsStorage
cd SecretsStorage
docker-compose up
```
Server will be avaible in <http://localhost>
You can chage port (default is 80) in docker-compose.yml.
