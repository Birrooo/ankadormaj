import requests

# URL pour récupérer les tags du dépôt GitHub
url = "https://api.github.com/repos/Birrooo/ankadormaj/tags"

# Effectuer la requête HTTP GET
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    tags = response.json()
    if tags:
        # Récupérer le premier tag (qui est généralement le plus récent)
        latest_version = tags[0]["name"]
        print(f"La dernière version disponible est : {latest_version}")
    else:
        print("Aucun tag trouvé.")
else:
    print(f"Erreur lors de la récupération des tags : {response.status_code}")
