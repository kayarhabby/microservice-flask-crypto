from flask import Flask, request, jsonify
from app.auth import generate_token
from app.crypto_utils import encrypt_bytes, decrypt_bytes
from codecs import decode

app = Flask(__name__)

STORAGE = {}  # file_id -> blob
TOKENS = {}   # token -> username

@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username", "alice")
    token = generate_token(username)
    TOKENS[token] = username
    return jsonify({"token": token}), 200

@app.route("/upload", methods=["POST"])
def upload():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "missing token"}), 401
    token = auth.split(" ", 1)[1]
    if token not in TOKENS:
        return jsonify({"error": "invalid token"}), 403

    username = TOKENS[token]

    f = request.files.get("file")
    if f is None:
        return jsonify({"error": "no file uploaded"}), 400

    blob = encrypt_bytes(f.read(), username)  # chiffrement avec clé utilisateur
    print(blob.decode("latin1") + "\n")
    print("test \n")
    file_id = f"file-{len(STORAGE)+1}"
    STORAGE[file_id] = {"owner": username, "blob": blob}  # stocke propriétaire
    return jsonify({"file_id": file_id, "len": len(blob)}), 201


@app.route("/download/<file_id>", methods=["GET"])
def download(file_id):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "missing token"}), 401
    token = auth.split(" ", 1)[1]
    if token not in TOKENS:
        return jsonify({"error": "invalid token"}), 403

    username = TOKENS[token]
    entry = STORAGE.get(file_id)
    if entry is None:
        return jsonify({"error": "not found"}), 404

    if entry["owner"] != username:
        return jsonify({"error": "forbidden"}), 403  # seul le propriétaire peut déchiffrer

    blob = entry["blob"]
    data = decrypt_bytes(blob, username)
    return data, 200, {"Content-Type": "application/octet-stream"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

