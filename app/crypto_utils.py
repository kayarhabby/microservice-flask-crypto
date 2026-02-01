from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import hmac
import hashlib

def derive_user_key(username: str) -> bytes:
    """Crée une clé symétrique unique pour chaque utilisateur à partir de son username"""
    return hashlib.sha256(username.encode()).digest()

NONCE = b"\x00" * 12

def encrypt_bytes(data: bytes, username: str) -> bytes:
    key = derive_user_key(username)
    aes = AESGCM(key)
    ciphertext = aes.encrypt(NONCE, data, None)
    return NONCE + ciphertext

def decrypt_bytes(blob: bytes, username: str) -> bytes:
    """Déchiffre les données pour un utilisateur donné"""
    key = derive_user_key(username)
    aes = AESGCM(key)
    nonce = blob[:12]
    ciphertext = blob[12:]
    return aes.decrypt(nonce, ciphertext, associated_data=None)
