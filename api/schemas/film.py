from api.models.model import Film
from api.schemas import ma


#Auto generate a schema for Film models
#We can use this to serialize and validate film data
class FilmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Film

#Instantiate the schema for both a single film and many films
film_schema = FilmSchema()
films_schema = FilmSchema(many=True)