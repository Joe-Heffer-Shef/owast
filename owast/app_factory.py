import secrets

import flask

import owast.blueprints.main.views
import owast.blueprints.experiment.views
import owast.blueprints.artifact.views
import owast.blueprints.container.views
import owast.blueprints.blob.views


def create_app() -> flask.Flask:
    app = flask.Flask(__name__)

    # Register blueprints
    app.register_blueprint(owast.blueprints.main.views.blueprint)
    app.register_blueprint(owast.blueprints.experiment.views.blueprint)
    app.register_blueprint(owast.blueprints.artifact.views.blueprint)
    app.register_blueprint(owast.blueprints.container.views.blueprint)
    app.register_blueprint(owast.blueprints.blob.views.blueprint)

    # TODO LDAP authentication (Active Directory)

    # Generate random secret key
    app.secret_key = secrets.token_urlsafe()

    return app
