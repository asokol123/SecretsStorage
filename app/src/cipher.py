from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import typing

# code from https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
def get_key_from_password(password: bytes, salt: bytes) -> bytes:
    """Generated Fernet key from password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def Encrypt(secret: str, passphrase: str) -> typing.Tuple[bytes, bytes]:
    """Encrypts secret with given password and returns encrypted message and salt."""
    salt = os.urandom(16)
    secret = secret.encode()
    passphrase = passphrase.encode()
    key = get_key_from_password(passphrase, salt)
    f = Fernet(key)
    enc = f.encrypt(secret)
    return enc, salt

def Decrypt(enc: bytes, passphrase: str, salt: bytes) -> str:
    """Decrypts encrypted message."""
    try:
        passphrase = passphrase.encode()
        key = get_key_from_password(passphrase, salt)
        f = Fernet(key)
        secret = f.decrypt(enc)
        return secret.decode()
    except InvalidToken:
        return None
