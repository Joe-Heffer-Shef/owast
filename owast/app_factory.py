import os

import flask
import flask_pymongo
import flask_talisman
import flask_seasurf


def create_app(*args, **kwargs) -> flask.Flask:
    """
    Initialise web application
    """

    app = flask.Flask(__name__, *args, **kwargs)
    # Load settings
    app.config.from_object(os.getenv('FLASK_CONFIG_OBJECT',
                                     'owast.flaskconfig'))

    # Security plugin
    flask_talisman.Talisman(app,
                            content_security_policy_nonce_in="['script-src']")

    # Cross-site request forgery (CSRF) protection
    flask_seasurf.SeaSurf(app)

    # Configure NoSQL database
    app.config['MONGO_URI'] = os.environ['MONGO_URI']
    app.mongo = flask_pymongo.PyMongo(app)

    # TODO LDAP authentication (Active Directory)
    register_blueprints(app)

    return app


def register_blueprints(app: flask.Flask):
    """
    Load modular application
    https://flask.palletsprojects.com/en/2.0.x/blueprints/
    """

    import owast.blueprints.main.views
    import owast.blueprints.experiment.views
    import owast.blueprints.artifact.views
    import owast.blueprints.container.views
    import owast.blueprints.blob.views
    import owast.blueprints.tool.views
    import owast.blueprints.option.views
    import owast.blueprints.service.views
    import owast.blueprints.settings.views

    app.register_blueprint(owast.blueprints.main.views.blueprint)
    app.register_blueprint(owast.blueprints.experiment.views.blueprint)
    app.register_blueprint(owast.blueprints.artifact.views.blueprint)
    app.register_blueprint(owast.blueprints.container.views.blueprint)
    app.register_blueprint(owast.blueprints.blob.views.blueprint)
    app.register_blueprint(owast.blueprints.tool.views.blueprint)
    app.register_blueprint(owast.blueprints.option.views.blueprint)
    app.register_blueprint(owast.blueprints.service.views.blueprint)
    app.register_blueprint(owast.blueprints.settings.views.blueprint)
