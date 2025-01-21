from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import update, insert

from api.config import config
from api.models import db
from api.models.model import Film, Actor, film_actor
from api.schemas.film import film_schema, films_schema

#Create a Blueprint or module
#We can insert this into our flask app
films_router = Blueprint('films', __name__, url_prefix='/films')

#GET requests to the collection return a list of all films in the database
@films_router.get('/')
def read_all_films():
    films = Film.query.paginate(page=1, per_page=config.OBJECTS_PER_PAGE, error_out=False).items
    return films_schema.dump(films)

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

#{
# #    "description": "description of movie",
# #     "language_id": 1,
# #     "length": 79,
# #     "original_language_id": null,
# #     "rating": "PG",
# #     "release_year": 2001,
# #     "rental_duration": 3,
# #     "rental_rate": 0.97,
# #     "replacement_cost": 15.67,
# #     "special_features": "Deleted Scenes,Behind the Scenes",
# #     "title": "mov"
# # }

# UPDATE
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

#Update film to include actor
@films_router.put('/<film_id>/<actor_id>')
def update_film_actors(film_id, actor_id):
    film = Film.query.get(film_id)
    exists = False
    for actor in film.actor:
        if int(actor.actor_id) == int(actor_id):
            exists = True
    if not exists:
        query = insert(film_actor).values({"actor_id": actor_id, "film_id": film_id})

        db.session.execute(query)
        db.session.commit()
    else:
        print("That record already exists")

    film = Film.query.get(film_id)

    return film_schema.dump(film)

#DELETE
@films_router.delete('/<film_id>')
def delete_film(film_id):
    film = Film.query.get(film_id)
    db.session.delete(film)
    db.session.commit()

    return film_schema.dump(film)