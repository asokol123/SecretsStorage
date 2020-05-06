# SecretsStorage
Secrets storage with fastAPI

## General
This is similar to <https://onetimesecret.com/>, but JsonAPI only.
You can:
* Create note, optionally protect it with psasphrase and set timeout
* Get note. After getting it will be deleted.

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
