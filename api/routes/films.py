from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.models import db
from api.models.model import Film, Actor
from api.schemas.film import film_schema, films_schema

#Create a Blueprint or module
#We can insert this into our flask app
films_router = Blueprint('films', __name__, url_prefix='/films')

#GET requests to the collection return a list of all films in the database
@films_router.get('/')
def read_all_films():
    films = Film.query.all()
    for film in films:
        film.serialise()
    return films

#GET requests to a specific document in the collection return a single film
@films_router.get('/<film_id>')
def read_film(film_id):
    film = Film.query.get(film_id)
    return film_schema.dump(film)

#POST
#Get parsed request body, validate against schema, create new film model, insert the record, update database, serialize created film
@films_router.post('/')
def create_film():
    film_data = request.json

    try:
        film_schema.load(film_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    film = Film(**film_data)
    db.session.add(film)
    db.session.commit()

    return film_schema.dump(film)

#UPDATE
@films_router.put('/<film_id>')
def update_film(film_id):
    film = Film.query.get(film_id)

    title = request.json['title']
    description = request.json['description']
    release_year = request.json['release_year']
    language_id = request.json['language_id']
    original_language_id = request.json['original_language_id']
    rental_duration = request.json['rental_duration']
    rental_rate = request.json['rental_rate']
    length = request.json['length']
    replacement_cost = request.json['replacement_cost']
    rating = request.json['rating']
    special_features = request.json['special_features']

    film.title = title
    film.description = description
    film.release_year = release_year
    film.language_id = language_id
    film.original_language_id = original_language_id
    film.rental_duration = rental_duration
    film.rental_rate = rental_rate
    film.length = length
    film.replacement_cost = replacement_cost
    film.rating = rating
    film.special_features = special_features



    db.session.commit()

    return film_schema.dump(film)

#DELETE
@films_router.delete('/<film_id>')
def delete_film(film_id):
    film = Film.query.get(film_id)
    db.session.delete(film)
    db.session.commit()

    return film_schema.dump(film)