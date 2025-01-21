from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import insert

from api.config import config
from api.models import db
from api.models.actor import Actor
from api.models.film import film_actor
from api.schemas.actor import actor_schema, actors_schema

#Create a Blueprint or module
#We can insert this into our flask app
actors_router = Blueprint('actors', __name__, url_prefix='/actors')

#Get all actors with all films by page
@actors_router.get('/page/<page>')
def read_all_actors(page):
    actors = Actor.query.paginate(page=int(page), per_page=config.OBJECTS_PER_PAGE, error_out=False).items
    if not actors:
        return jsonify({"error": "No actors exist"})
    else:
        return actors_schema.dump(actors)

#Get specific actor with all films
@actors_router.get('/<actor_id>')
def read_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        return jsonify({"error": "That actor doesn't exist"})
    else:
        return actor_schema.dump(actor)

#POST
#Get data from request body, load into schema, make actor object, add to db
@actors_router.post('/')
def create_actor():
    actor_data = request.json

    try:
        actor_schema.load(actor_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    actor = Actor(**actor_data)
    db.session.add(actor)
    db.session.commit()

    return actor_schema.dump(actor)

# {
#             "first_name": "Jemima",
#             "last_name": "Stobart"
#         }

#Find actor by actor_id, take data from request body, change data in actor object to request data, commit to db
@actors_router.put('/<actor_id>')
def update_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        return jsonify({"error": "That actor doesn't exist"})
    else:
        first_name = request.json['first_name']
        last_name = request.json['last_name']

        actor.first_name = first_name
        actor.last_name = last_name

        db.session.commit()

        return actor_schema.dump(actor)

#Update film_actor table to include new relationship between actor and film
@actors_router.put('/<actor_id>/<film_id>')
def update_actor_films(film_id, actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        return jsonify({"error": "That actor doesn't exist"})
    else:
        exists = False
        for film in actor.film:
            if int(film.film_id) == int(film_id):
                exists = True
        if not exists:
            query = (insert(film_actor).values({"actor_id": actor_id, "film_id": film_id}))
            db.session.execute(query)
            db.session.commit()
        else:
            print("That record already exists")

        actor = Actor.query.get(actor_id)
        if not actor:
            return jsonify({"error": "That actor doesn't exist"})
        else:
            return actor_schema.dump(actor)

#Find actor, delete actor
@actors_router.delete('/<actor_id>')
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        return jsonify({"error": "That actor doesn't exist"})
    else:
        db.session.delete(actor)
        db.session.commit()

        return actor_schema.dump(actor)