import os
import secrets

import flask
import flask_pymongo
import pymongo.database

import owast.blueprints.main.views
import owast.blueprints.experiment.views
import owast.blueprints.artifact.views
import owast.blueprints.container.views
import owast.blueprints.blob.views


def create_app(*args, **kwargs) -> flask.Flask:
    """
    Initialise web application
    """

    app = flask.Flask(__name__, *args, **kwargs)

    # Register blueprints
    # https://flask.palletsprojects.com/en/2.0.x/blueprints/
    app.register_blueprint(owast.blueprints.main.views.blueprint)
    app.register_blueprint(owast.blueprints.experiment.views.blueprint)
    app.register_blueprint(owast.blueprints.artifact.views.blueprint)
    app.register_blueprint(owast.blueprints.container.views.blueprint)
    app.register_blueprint(owast.blueprints.blob.views.blueprint)

    # TODO LDAP authentication (Active Directory)

    # Generate random secret key
    app.secret_key = secrets.token_urlsafe()

    # Initialise Flask-PyMongo plugin
    # https://flask-pymongo.readthedocs.io/en/latest/#quickstart
    app.config['MONGO_URI'] = os.environ['MONGO_URI']
    app.mongo = flask_pymongo.PyMongo(app)

    return app
