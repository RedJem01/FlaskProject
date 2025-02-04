from sqlalchemy.orm import validates

from api.models import db

film_actor = db.Table(
    "film_actor",
    db.Column("actor_id", db.Integer, db.ForeignKey("actor.actor_id")),
    db.Column("film_id", db.Integer, db.ForeignKey("film.film_id")))


#A model of our actor table
# @dataclasses.dataclass
class Film(db.Model):
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
    actor = db.relationship('Actor', secondary=film_actor, back_populates='film', cascade='all, delete')

    @validates('title')
    def convert_upper(self, key, value):
        return value.upper()