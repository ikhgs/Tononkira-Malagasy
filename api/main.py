import os
from flask import Flask, jsonify, request
from requests_html import HTMLSession

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Tononkira Scraper!"

@app.route('/search', methods=['GET'])
def search_chanteur():
    # Récupérer le nom du chanteur depuis les paramètres GET
    chanteur = request.args.get('chanteur')

    # Vérifier si le paramètre existe
    if not chanteur:
        return jsonify({"message": "Veuillez fournir le nom d'un chanteur."}), 400

    # Créer une session HTML
    s = HTMLSession()

    # URL de recherche avec le nom du chanteur
    url = f'https://tononkira.serasera.org/tononkira?lohateny={chanteur}'

    # Faire une requête GET
    r = s.get(url)

    # Vérifier si la requête a réussi
    if r.status_code != 200:
        return jsonify({"message": "Impossible d'accéder au site Tononkira."}), 500

    # Extraire les chansons depuis le contenu HTML
    songs = r.html.find('a.m')  # Mettre à jour ce sélecteur si nécessaire

    # Si aucune chanson n'est trouvée
    if not songs:
        return jsonify({"message": f"Aucune chanson trouvée pour ce chanteur : {chanteur}"}), 404

    # Lister les chansons et leurs liens
    song_list = []
    for song in songs:
        title = song.text.strip()
        href = song.attrs['href']
        full_url = f"https://tononkira.serasera.org{href}"
        song_list.append({
            'title': title,
            'link': full_url
        })

    # Retourner les données en format JSON
    return jsonify(song_list)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
