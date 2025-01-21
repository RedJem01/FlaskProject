from api.models.model import Film
from api.schemas import ma

from marshmallow_sqlalchemy import fields


#Auto generate a schema for Film models
#We can use this to serialize and validate film data
class FilmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        fields = ("film_id", "description", "language_id", "length", "original_language_id", "rating",
                  "release_year", "rental_duration", "rental_rate", "replacement_cost",
                  "special_features", "title", "actor")

    actor = fields.Nested('ActorSchema', many=True, exclude=('film',))

#Instantiate the schema for both a single film and many films
film_schema = FilmSchema()
films_schema = FilmSchema(many=True)