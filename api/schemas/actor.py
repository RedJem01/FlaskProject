from marshmallow_sqlalchemy import fields

from api.models.model import Actor
from api.schemas import ma


#Auto generate a schema for Actor models
#We can use this to serialize and validate actor data
class ActorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Actor
        fields = ("actor_id", "first_name", "last_name", "film")

    # film = fields.Nested('FilmSchema', many = True)

#Instantiate the schema for both a single actor and many actors
actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)