from sqlalchemy.orm import validates

from api.models import db
from api.models.film import film_actor

#A model of our actor table
# @dataclasses.dataclass
class Actor(db.Model):
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    film = db.relationship('Film', secondary=film_actor, back_populates='actor', cascade='all, delete')

    @validates('first_name', 'last_name')
    def convert_upper(self, key, value):
        return value.upper()