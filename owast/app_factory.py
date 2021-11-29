import os
import pathlib
import itertools

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
    root = pathlib.Path('owast/blueprints')

    # Iterate over modules
    for path in root.iterdir():
        if path.is_dir() and not path.name.startswith('_'):
            # Build module name
            module = '.'.join(itertools.chain(path.parts, ['views']))
            # Dynamically import and register blueprint
            exec(f'import {module}')
            app.register_blueprint(eval(f'{module}.blueprint'))
