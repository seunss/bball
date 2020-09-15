from flask import Flask
from flask import request, jsonify, redirect, url_for, flash, render_template, send_file, safe_join, abort, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://tjadhigvrltwzk:43809a6ba156405f161e0184ab305d44fc6cfeae18e0fa82177d3f0712ac38b0@ec2-35-153-12-59.compute-1.amazonaws.com:5432/d8n2b7cc3lmoqs"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Allow only pictures to be uploaded
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/images'
#UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')

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




@app.route('/')
def test():
     safe_path = safe_join(app.config["UPLOAD_FOLDER"], 'testimage.jpg')
     return  send_from_directory(app.config['UPLOAD_FOLDER'],'testimage.jpg')

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
            newPlayer = PlayersModel(
                name=data['name'], sport=data['sport'], skillLevel=data['skill'], imageLoc=  filename)
            db.session.add(newPlayer)
            db.session.commit()
            return jsonify( "player successfully")
        
            
@app.route('/allplayers',methods = ['GET'])
def get_all():
     if request.method == 'GET':
        players = PlayersModel.query.all()

            
        
        

        results = [
            {
                "name": player.name,
                "model": player.sport,
                "skill": player.skillLevel,
                "id": players.id
            } for player in players]
        return jsonify(results)


@app.route('/players/<player_id>', methods=['GET', 'PUT', 'DELETE']) # Getting a single players info
def handle_player(player_id):
    player = PlayersModel.query.get_or_404(player_id)

    if request.method == 'GET':
        response = {
            "name": player.name,
            "sport": player.sport,
            "skill": player.skillLevel,
            "imageLoc": player.id
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


@app.route('/iamges/<player_id>')
def get_image(player_id):
    player = PlayersModel.query.get_or_404(player_id)

    if request.method == 'GET':
        safe_path = safe_join(app.config["UPLOAD_FOLDER"], player.imageLoc)

    try:
        return send_file(safe_path)
    except FileNotFoundError:
        abort(404)






if __name__ == '__main__':
    app.run(debug=True)
