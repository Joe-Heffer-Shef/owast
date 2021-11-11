"""
Gunicorn config file

Config file docs:
https://docs.gunicorn.org/en/stable/configure.html#configuration-file

Settings:
https://docs.gunicorn.org/en/stable/settings.html#settings
"""

import multiprocessing

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() + 1
chdir = '/'
wsgi_app = 'owast.app_factory:create_app()'
user = 'www-data'
group = 'www-data'
