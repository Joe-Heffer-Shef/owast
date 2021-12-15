import os
import pathlib
import itertools
import json

import flask
import flask_pymongo
import flask_talisman
import flask_seasurf
import flask_login


def create_app(*args, **kwargs) -> flask.Flask:
    """
    Initialise web application
    """

    app = flask.Flask(__name__, *args, **kwargs)
    # Load settings
    app.config.from_object(os.getenv('FLASK_CONFIG_OBJECT',
                                     'owast.flaskconfig'))
    app.config['BLUEPRINTS_DIR'] = os.environ['BLUEPRINTS_DIR']

    # Security plugin
    flask_talisman.Talisman(app,
                            content_security_policy_nonce_in="['script-src']")

    # Cross-site request forgery (CSRF) protection
    flask_seasurf.SeaSurf(app)

    # Register user authentication plugin

    # Configure NoSQL database
    app.config['MONGO_URI'] = os.environ['MONGO_URI']
    app.mongo = flask_pymongo.PyMongo(app)

    # TODO LDAP authentication (Active Directory)
    register_login_manager(app)
    register_blueprints(app)
    register_jinja_globals(app)

    return app


def register_blueprints(app: flask.Flask, blueprints_dir: pathlib.Path = None):
    """
    Load modular application
    https://flask.palletsprojects.com/en/2.0.x/blueprints/
    """

    # Root directory to search for blueprints
    blueprints_dir = pathlib.Path(
        blueprints_dir or app.config['BLUEPRINTS_DIR'])

    # Iterate over modules
    for path in blueprints_dir.iterdir():
        if path.is_dir() and not path.name.startswith('_'):
            # Build module name
            module = '.'.join(itertools.chain(path.parts, ['views']))
            # Dynamically import and register blueprint
            exec(f'import {module}')
            blueprint = f'{module}.blueprint'
            app.register_blueprint(eval(blueprint))
            app.logger.debug(f"Registered blueprint '{blueprint}'")


def register_jinja_globals(app: flask.Flask):
    jinja_globals = json.loads(
        os.environ.get('JINJA_GLOBALS', '{}'))  # type: dict

    for name, value in jinja_globals.items():
        app.jinja_env.globals[name] = value
        app.logger.info(f"Set Jinja template global {name}: '{value}'")


def register_login_manager(app: flask.Flask):
    """
    https://flask-login.readthedocs.io/en/latest/#how-it-works
    """
    login_manager = flask_login.LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        from .blueprints.user.models import User
        return User(user_id)
