Exemples d'utilisation du micro-service Flask

1. Lancement du micro-service

# Depuis le répertoire racine du projet

    a. Créer un environnement virtuel python : 
        python3 -m venv .venv
        source .venv/bin/activate -> Linux
        .\.venv\Scripts\Activate.ps1 -> windows

    b. Installer les dépendances :
        pip install -r requirements.txt

    c. Lancer le micro-service :
        python3 -m app.app

Le service tourne sur http://127.0.0.1:5000

(Toutes les commandes suivantes sont à utiliser dans un autre terminal que celui dans lequel vous avez lancé le service)

2. Tester /login et récupérer un token

curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username":"alice"}'

Réponse attendue :
{"token":"svuV4GOAjI0rPfDWePTto0xJKmlf8P7vJgdjkVgBPds"}

3. Upload d'un fichier

# Remplacer <votre_token> par le token obtenu précédemment
TOKEN="<votre_token>"
curl -X POST "http://127.0.0.1:5000/upload" `
  -H "Authorization: $env:TOKEN" `
  -F "file=@exemple.txt"

Réponse attendue :
{"status":"file stored securely"}

4. Télécharger un fichier

curl -X GET "http://127.0.0.1:5000/download" `
  -H "Authorization: $env:TOKEN" `
  -o file.txt

Réponse attendue : Contenu du fichier ou une erreur d'autorisation 

Pour que la sortie soit mise dans un fichier, rajouter :
-o output.txt


