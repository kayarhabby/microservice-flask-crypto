from flask import Flask, request, jsonify, send_file, abort
import io
import time

from app.auth import generate_token, verify_token
from app.crypto_utils import encrypt_bytes, decrypt_bytes

app = Flask(__name__)

FILES = {}

# ======================
# HEADERS DE SÉCURITÉ
# ======================

@app.after_request
def set_security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'"
    )
    response.headers["Permissions-Policy"] = (
        "geolocation=(), microphone=(), camera=(), fullscreen=()"
    )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    # Supprime la fuite Werkzeug
    response.headers.pop("Server", None)

    return response


# ======================
# ROUTES
# ======================

@app.route("/", methods=["GET"])
def index():
    return "Microservice Flask sécurisé"


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or "username" not in data:
        abort(400)

    token = generate_token(data["username"])
    return jsonify({"token": token})


@app.route("/upload", methods=["POST"])
def upload():
    token = request.headers.get("Authorization")
    if not token:
        abort(401)

    user = verify_token(token)
    if not user:
        abort(403)

    if "file" not in request.files:
        abort(400)

    file = request.files["file"]
    plaintext = file.read()

    encrypted = encrypt_bytes(user, plaintext)
    FILES[user] = encrypted

    return jsonify({"status": "file stored securely"})


@app.route("/download", methods=["GET"])
def download():
    token = request.headers.get("Authorization")
    if not token:
        abort(401)

    user = verify_token(token)
    if not user:
        abort(403)

    encrypted = FILES.get(user)
    if not encrypted:
        abort(404)

    plaintext = decrypt_bytes(user, encrypted)

    return send_file(
        io.BytesIO(plaintext),
        as_attachment=True,
        download_name="file.txt"
    )


# ======================
# LANCEMENT
# ======================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
