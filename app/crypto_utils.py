import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Secret serveur (doit être stocké dans une variable d'environnement en pratique)
SERVER_SECRET = b"super-secret-server-key-change-me"

def derive_user_key(username: str, salt: bytes) -> bytes:
    """
    Dérive une clé AES à partir du nom d'utilisateur + secret serveur.
    Utilise PBKDF2-HMAC-SHA256.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
    )
    return kdf.derive(username.encode() + SERVER_SECRET)


def encrypt_bytes(username: str, plaintext: bytes) -> bytes:
    """
    Chiffrement AES-GCM avec nonce aléatoire.
    Format de sortie : salt || nonce || ciphertext
    """
    salt = os.urandom(16)
    key = derive_user_key(username, salt)

    aesgcm = AESGCM(key)
    nonce = os.urandom(12)

    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return salt + nonce + ciphertext


def decrypt_bytes(username: str, blob: bytes) -> bytes:
    """
    Déchiffrement AES-GCM.
    """
    salt = blob[:16]
    nonce = blob[16:28]
    ciphertext = blob[28:]

    key = derive_user_key(username, salt)
    aesgcm = AESGCM(key)

    return aesgcm.decrypt(nonce, ciphertext, None)
