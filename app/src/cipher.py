import hashlib
import typing
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def AESEncrypt(message: str, key: str) -> (bytes, bytes):
    """Returns encrypted message and iv"""
    block_size = AES.block_size
    key = hashlib.sha256(key.encode()).digest()
    message = pad(message.encode(), block_size)
    iv = Random.new().read(block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc = cipher.encrypt(message)
    return (enc, iv)

def AESDecrypt(enc: bytes, key: str, iv: bytes) -> typing.Optional[str]:
    """Returns decrypted message or None if failed to decrypt"""
    try:
        block_size = AES.block_size
        key = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        message = cipher.decrypt(enc)
        return unpad(message, block_size).decode()
    except (KeyboardInterrupt, SystemExit):
        raise
    # To prevent padding oracle and everything like that
    except Exception as e:
        return None
