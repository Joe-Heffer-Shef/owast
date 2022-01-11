# Flask configuration
# https://flask.palletsprojects.com/en/2.0.x/config/#builtin-configuration-values

import os

SECRET_KEY = os.environ['SECRET_KEY']
SERVER_NAME = os.getenv('SERVER_NAME')
PREFERRED_URL_SCHEME = os.getenv('PREFERRED_URL_SCHEME')
BLUEPRINTS_DIR = os.environ['BLUEPRINTS_DIR']
MONGO_URI = os.environ['MONGO_URI']
