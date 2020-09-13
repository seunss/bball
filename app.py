from flask import Flask
from flask import request, jsonify, redirect, url_for, flash, render_template, send_file, safe_join, abort
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:ginger@localhost:5432/cars_api"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Allow only pictures to be uploaded
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class PlayersModel(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    sport = db.Column(db.String())
    skillLevel = db.Column(db.Integer())
    imageLoc = db.Column(db.String())

    def __init__(self, name, sport, skillLevel, imageLoc):
        self.name = name
        self.sport = sport
        self.skillLevel = skillLevel
        self.imageLoc = imageLoc

    def __repr__(self):
        return f"<Player {self.name}>"






@app.route('/addplayer', methods = ['POST'])
def add_player():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify('no file found')

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("seun")
            data = request.form
            newCar = PlayersModel(
                name=data['name'], sport=data['sport'], skillLevel=data['skill'], imageLoc=  filename)
            db.session.add(newCar)
            db.session.commit()
            return jsonify( "player successfully")
        
            

@app.route('/players/<player_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_player(player_id):
    player = PlayersModel.query.get_or_404(player_id)

    if request.method == 'GET':
        response = {
            "name": player.name,
            "sport": player.sport,
            "skill": player.skillLevel
        }
        return {"message": "success", "player": response}

    elif request.method == 'PUT':
        data = request.get_json()
        player.name = data['name']
        player.model = data['model']
        player.skillLevel = data['skill']
        db.session.add(player)
        db.session.commit()
        return {"message": f"Player {player.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(player)
        db.session.commit()
        return {"message": f"Player {player.name} successfully deleted."}


@app.route('/iamges/<player_id>', methods=['GET'])
def get_image(player_id):
    player = PlayersModel.query.get_or_404(player_id)

    if request.method == 'GET':
        safe_path = safe_join(app.config["UPLOAD_FOLDER"], player.imageLoc)

    try:
        return send_file(safe_path)
    except FileNotFoundError:
        abort(404)
        return player.imageLoc






if __name__ == '__main__':
    app.run(debug=True)
