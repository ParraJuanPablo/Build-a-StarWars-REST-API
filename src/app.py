"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_charactes():

    selected_characters = Character.query.all()

    return jsonify(selected_characters), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):

    selected_character = Character.query.get(people_id)

    return jsonify(selected_character.serialize), 200

@app.route('/planets', methods=['GET'])
def get_planes():

    selected_planets = Planet.query.all()

    return jsonify(selected_planets), 200

@app.route('/people/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    selected_planet = Planet.query.get(planet_id)

    return jsonify(selected_planet.serialize), 200

@app.route('/users', methods=['GET'])
def get_users():

    selected_users = User.query.all()

    return jsonify(selected_users), 200

@app.route('/users/<int:user>/favorites', methods=['GET'])
def get_user_favorites(user):

    selected_user_favorites = Favorites.query.filter_by(user_id == user)

    return jsonify(selected_user_favorites), 200

@app.route('/users/<int:user>/favorites/planet/<int:planet_id>', methods=['POST'])
def add_user_favorites_planets(user, planet_id):

    user_id = user
    object_id = planet_id

    favorite = Favorites(user_id=user, object_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "added to favs"}), 200

@app.route('/users/<int:user>/favorites/people/<int:people_id>', methods=['POST'])
def add_user_favorites_characters(user, people_id):

    user_id = user
    object_id = people_id

    favorite = Favorites(user_id=user, object_id=people_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "added to favs"}), 200

@app.route('/users/<int:user>/favorites/planet/<int:planet_id>', methods=['DELETE'])
def add_user_favorites_planets(user, planet_id):

    Favorites.query.filter_by(user_id == user, object_id=planet_id).delete()

    db.session.commit()

    return jsonify({"msg": "deleted from favs"}), 200

@app.route('/users/<int:user>/favorites/people/<int:people_id>', methods=['DELETE'])
def add_user_favorites_characters(user, people_id):

    Favorites.query.filter_by(user_id == user, object_id=people_id).delete()

    db.session.commit()

    return jsonify({"msg": "deleted from favs"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
