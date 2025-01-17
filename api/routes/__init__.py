from flask import Blueprint

from api.routes.actors import actors_router

#Create a routes model to be registered in our app
routes = Blueprint('api', __name__, url_prefix='/api')

#Register our nested routes
routes.register_blueprint(actors_router)