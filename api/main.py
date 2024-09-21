from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Route pour rechercher les chansons d'un chanteur
@app.route('/search', methods=['GET'])
def search_songs():
    chanteur = request.args.get('chanteur')
    if not chanteur:
        return jsonify({'error': 'Chanteur non spécifié'}), 400

    # URL du site à scraper avec le nom du chanteur
    url = f"https://tononkira.serasera.org/tononkira?lohateny={chanteur}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Impossible d\'accéder à la page'}), 500
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraire les chansons listées
    song_list = []
    songs = soup.find_all('a', class_='m')
    
    for song in songs:
        title = song.text.strip()
        href = song['href']
        song_list.append({'title': title, 'link': f"https://tononkira.serasera.org{href}"})
    
    if not song_list:
        return jsonify({'message': 'Aucune chanson trouvée pour ce chanteur'}), 404

    return jsonify({'chanteur': chanteur, 'chansons': song_list})

# Route pour afficher les détails d'une chanson
@app.route('/song', methods=['GET'])
def get_song():
    song_url = request.args.get('url')
    if not song_url:
        return jsonify({'error': 'URL de la chanson non spécifiée'}), 400

    response = requests.get(song_url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Impossible d\'accéder à la page'}), 500
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraire les détails de la chanson
    song_title = soup.find('h1').text.strip()
    lyrics = soup.find('div', {'id': 'songLyric'}).text.strip()

    return jsonify({'title': song_title, 'lyrics': lyrics})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
