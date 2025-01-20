from sqlalchemy_serializer import SerializerMixin

from api.models import db


film_actor = db.Table(
    "film_actor",
    db.Column("actor_id", db.Integer, db.ForeignKey("actor.actor_id")),
    db.Column("film_id", db.Integer, db.ForeignKey("film.film_id")))

#A model of our actor table
# @dataclasses.dataclass
class Actor(db.Model, SerializerMixin):
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    film = db.relationship('Film', secondary=film_actor, back_populates='actor')

    # serialize_rules = ("-film.actor",)
    def serialise(self):
        return {
            "actor_id": self.actor_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "film": [f.actorSerialise() for f in self.film]
        }

    def filmSerialise(self):
        return {
            "actor_id": self.actor_id,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

#A model of our actor table
# @dataclasses.dataclass
class Film(db.Model, SerializerMixin):
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    language_id = db.Column(db.Integer, nullable=False)
    original_language_id = db.Column(db.Integer, nullable=True)
    rental_duration = db.Column(db.Integer, nullable=False)
    rental_rate = db.Column(db.Double, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    replacement_cost = db.Column(db.Double, nullable=False)
    rating = db.Column(db.String(255), nullable=False)
    special_features = db.Column(db.String(255), nullable=False)
    actor = db.relationship('Actor', secondary=film_actor, back_populates='film')

    # serialize_rules = ("-actor.film",)

    def serialise(self):
        return {
            "film_id": self.film_id,
            "title": self.title,
            "description": self.description,
            "release_year": self.release_year,
            "language_id": self.language_id,
            "original_language_id": self.original_language_id,
            "rental_duration": self.rental_duration,
            "rental_rate": self.rental_rate,
            "length": self.length,
            "replacement_cost": self.replacement_cost,
            "rating": self.rating,
            "special_features": self.special_features,
            "actor": [a.filmSerialise() for a in self.actor]
        }

    def actorSerialise(self):
        return {
            "film_id": self.film_id,
            "title": self.title,
            "description": self.description,
            "release_year": self.release_year,
            "language_id": self.language_id,
            "original_language_id": self.original_language_id,
            "rental_duration": self.rental_duration,
            "rental_rate": self.rental_rate,
            "length": self.length,
            "replacement_cost": self.replacement_cost,
            "rating": self.rating,
            "special_features": self.special_features
        }