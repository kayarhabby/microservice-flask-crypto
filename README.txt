Exemples d'utilisation du micro-service Flask

1. Lancement du micro-service

# Depuis le répertoire racine du projet

    a. Créer un environnement virtuel python : 
        python3 -m venv .venv
        source .venv/bin/activate

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
{"token":"alice-<timestamp>-<random>"}

Par exemple : "token": "alice-1767879085-8103900"

3. Upload d'un fichier

# Remplacer <votre_token> par le token obtenu précédemment
TOKEN="<votre_token>"
curl -X POST http://127.0.0.1:5000/upload \
-H "Authorization: Bearer $TOKEN" \
-F "file=@./exemple.txt"

Réponse attendue :
{"file_id":"file-1" 
"len":61}

4. Télécharger un fichier

curl -X GET http://127.0.0.1:5000/download/file-1 \
-H "Authorization: Bearer $TOKEN" 

Réponse attendue : Contenu du fichier ou une erreur d'autorisation 

Pour que la sortie soit mise dans un fichier, rajouter :
-o output.txt


