from flask import Flask, request, jsonify, render_template, redirect, url_for
import uuid

app = Flask(__name__)

filmy = []

def generuj_id():
    return str(uuid.uuid4())

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', filmy=filmy)

@app.route('/dodaj_film', methods=['POST'])
def dodaj_film():
    data = request.form
    nowy_film = {
        'id': generuj_id(),
        'tytul': data['tytul'],
        'rok_wydania': int(data['rok_wydania']),
        'gatunek': data['gatunek']
    }
    filmy.append(nowy_film)
    return redirect(url_for('index'))

@app.route('/usun_film/<string:film_id>', methods=['POST'])
def usun_film(film_id):
    filmy_do_usuniecia = [film for film in filmy if film['id'] == film_id]
    if filmy_do_usuniecia:
        filmy.remove(filmy_do_usuniecia[0])
    return redirect(url_for('index'))

@app.route('/edytuj_film/<string:film_id>', methods=['GET'])
def edytuj_film(film_id):
    film_do_edytowania = [film for film in filmy if film['id'] == film_id]
    if film_do_edytowania:
        return render_template('edytuj.html', film=film_do_edytowania[0])
    else:
        return "Film nie istnieje"

@app.route('/zapisz_edycje', methods=['POST'])  # Poprawiono metodę na POST
def zapisz_edycje():
    film_id = request.form['film_id']
    nowy_tytul = request.form['tytul']
    nowy_rok_wydania = int(request.form['rok_wydania'])
    nowy_gatunek = request.form['gatunek']

    for film in filmy:
        if film['id'] == film_id:
            film['tytul'] = nowy_tytul
            film['rok_wydania'] = nowy_rok_wydania
            film['gatunek'] = nowy_gatunek
            break

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)