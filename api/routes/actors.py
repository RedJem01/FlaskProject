from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.models import db
from api.models.model import Actor, Film
from api.schemas.actor import actor_schema, actors_schema

#Create a Blueprint or module
#We can insert this into our flask app
actors_router = Blueprint('actors', __name__, url_prefix='/actors')

#GET requests to the collection return a list of all actors in the database
@actors_router.get('/')
def read_all_actors():
    actors = Actor.query.all()
    result = actors_schema.dump(actors)
    return jsonify(result)

#GET requests to a specific document in the collection return a single actor
@actors_router.get('/<actor_id>')
def read_actor(actor_id):
    actor = Actor.query.get(actor_id)
    return actor_schema.dump(actor)

#POST
#Get parsed request body, validate against schema, create new actor model, insert the record, update database, serialize created actor
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

#UPDATE
@actors_router.put('/<actor_id>')
def update_actor(actor_id):
    actor = Actor.query.get(actor_id)

    first_name = request.json['first_name']
    last_name = request.json['last_name']

    actor.first_name = first_name
    actor.last_name = last_name

    db.session.commit()

    return actor_schema.dump(actor)

#DELETE
@actors_router.delete('/<actor_id>')
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    db.session.delete(actor)
    db.session.commit()

    return actor_schema.dump(actor)