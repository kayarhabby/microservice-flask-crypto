import secrets
import time

TOKEN_EXPIRATION = 3600  # 1 heure
TOKENS = {}

def generate_token(username: str) -> str:
    token = secrets.token_urlsafe(32)
    TOKENS[token] = {
        "user": username,
        "expires": time.time() + TOKEN_EXPIRATION
    }
    return token


def verify_token(token: str):
    entry = TOKENS.get(token)
    if not entry:
        return None

    if time.time() > entry["expires"]:
        TOKENS.pop(token, None)
        return None

    return entry["user"]
