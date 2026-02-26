import base64
from hashlib import sha256
from secrets import token_bytes

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .config import get_settings


def _build_key_bytes() -> bytes:
    settings = get_settings()
    configured_key = settings.habits_encryption_key.strip()
    if configured_key:
        try:
            decoded = base64.urlsafe_b64decode(configured_key.encode('utf-8'))
            if len(decoded) == 32:
                return decoded
        except Exception:
            pass
        if len(configured_key) == 64:
            try:
                return bytes.fromhex(configured_key)
            except ValueError:
                pass
        return sha256(configured_key.encode('utf-8')).digest()
    return sha256(settings.jwt_secret_key.encode('utf-8')).digest()


def encrypt_number(value: float) -> bytes:
    plaintext = f'{value:.8f}'.encode('utf-8')
    nonce = token_bytes(12)
    ciphertext = AESGCM(_build_key_bytes()).encrypt(nonce, plaintext, None)
    return nonce + ciphertext


def decrypt_number(value: bytes) -> float:
    nonce = value[:12]
    ciphertext = value[12:]
    plaintext = AESGCM(_build_key_bytes()).decrypt(nonce, ciphertext, None)
    return float(plaintext.decode('utf-8'))
