import os
import secrets

import flask
import pymodm


def create_app(*args, **kwargs) -> flask.Flask:
    """
    Initialise web application
    """

    app = flask.Flask(__name__, *args, **kwargs)
    register_blueprints(app)

    # TODO LDAP authentication (Active Directory)

    # Generate random secret key
    app.secret_key = secrets.token_urlsafe()

    # Connect to metadata
    pymodm.connect(os.environ['MONGO_URI'])

    return app


def register_blueprints(app: flask.Flask):
    """
    https://flask.palletsprojects.com/en/2.0.x/blueprints/
    """

    import owast.blueprints.main.views
    import owast.blueprints.experiment.views
    import owast.blueprints.artifact.views
    import owast.blueprints.container.views
    import owast.blueprints.blob.views

    app.register_blueprint(owast.blueprints.main.views.blueprint)
    app.register_blueprint(owast.blueprints.experiment.views.blueprint)
    app.register_blueprint(owast.blueprints.artifact.views.blueprint)
    app.register_blueprint(owast.blueprints.container.views.blueprint)
    app.register_blueprint(owast.blueprints.blob.views.blueprint)
