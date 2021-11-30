"""
Gunicorn config file

Config file docs:
https://docs.gunicorn.org/en/stable/configure.html#configuration-file

Settings:
https://docs.gunicorn.org/en/stable/settings.html#settings
"""

import os

wsgi_app = os.getenv('WSGI_APP')

# TODO security config
