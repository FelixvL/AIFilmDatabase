from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuratie van de database 
# Zorg ervoor dat je de gebruikersnaam, het wachtwoord en de databasenaam invult die je in MAMP hebt ingesteld.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/filmdb'

db = SQLAlchemy(app)

class Acteur(db.Model):
    __tablename__ = 'acteurs' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voornaam = db.Column(db.String(100))
    achternaam = db.Column(db.String(100))
    # Vul hier de rest van je velden in

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(100))
    bestandsnaam = db.Column(db.String(100))
    # Voeg hier andere velden toe die je wilt opslaan voor een film

    def __init__(self, naam, bestandsnaam):
        self.naam = naam
        self.bestandsnaam = bestandsnaam
        # Initialiseer andere velden indien nodig

    def to_dict(self):
        return {
            'id': self.id,
            'naam': self.naam,
            'bestandsnaam': self.bestandsnaam
            # Voeg andere velden toe die je wilt opnemen in de dict-representatie
        }

@app.route('/acteurs', methods=['GET', 'POST'])
def handle_acteurs():
    if request.method == 'POST':
        data = request.json
        acteur = Acteur(voornaam=data['voornaam'], achternaam=data['achternaam'])  # Vul hier de rest van je velden in
        db.session.add(acteur)
        db.session.commit()
        return {"message": "Acteur succesvol toegevoegd."}, 201

    elif request.method == 'GET':
        acteurs = Acteur.query.all()
        return jsonify([acteur.to_dict() for acteur in acteurs])

@app.route('/films', methods=['POST'])
def create_film():
    data = request.get_json()
    naam = data.get('naam')
    bestandsnaam = data.get('bestandsnaam')

    film = Film(naam=naam, bestandsnaam=bestandsnaam)
    db.session.add(film)
    db.session.commit()

    return jsonify({'message': 'Film succesvol toegevoegd'})
@app.route('/films', methods=['GET'])
def get_films():
    films = Film.query.all()
    film_list = [film.to_dict() for film in films]
    return jsonify(film_list)




@app.route('/video/<video_id>')
def get_video(video_id):
    video = Film.query.get(video_id)

    if video is None:
        return jsonify({'error': 'Video not found'}), 404

    video_data = {
        'id': video.id,
        'naam': video.naam,
        'bestandsnaam': video.bestandsnaam
    }

    return jsonify(video_data)
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
