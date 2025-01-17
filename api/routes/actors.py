from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.models import db
from api.models.actor import Actor
from api.schemas.actor import actor_schema, actors_schema

#Create a Blueprint or module
#We can insert this into our flask app
actors_router = Blueprint('actors', __name__, url_prefix='/actors')

#GET requests to the collection return a list of all actors in the database
@actors_router.get('/')
def read_all_actors():
    actors = Actor.query.all()
    return actors_schema.dump(actors)

#GET requests to a specific document in the collection return a single actor
@actors_router.get('/<actor_id>')
def read_actor(actor_id):
    actor = Actor.query.get(actor_id)
    return actor_schema.dump(actor)

#POST
#Get parsed request body, validate against schema, create new actor model, insert the record, update databse, serialize created actor
@actors_router.post('/')
def create_actor():
    actor_data = request.json

    try:
        actor_schema.load(actor_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    actor = Actor(**actor_data)
    db.seesion.add(actor)
    db.session.commit()

    return actor_schema.dump(actor)