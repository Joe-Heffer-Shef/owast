"""
Gunicorn config file

Config file docs:
https://docs.gunicorn.org/en/stable/configure.html#configuration-file

Settings:
https://docs.gunicorn.org/en/stable/settings.html#settings
"""

import os
import multiprocessing
import distutils.util

bind = os.getenv('BIND', '0.0.0.0:8000')
workers = int(os.getenv('WORKERS', multiprocessing.cpu_count()))
chdir = os.getenv('CHDIR', '/')
wsgi_app = os.getenv('WSGI_APP', 'owast.app_factory:create_app()')
user = os.getenv('USER', 'www-data')
group = os.getenv('GROUP', 'www-data')

# Debugging
# https://docs.gunicorn.org/en/stable/settings.html#debugging
reload = bool(distutils.util.strtobool(os.getenv('RELOAD', 'False')))
print_config = bool(
    distutils.util.strtobool(os.getenv('PRINT_CONFIG', 'False')))

# Logging
# https://docs.gunicorn.org/en/stable/settings.html#logging
accesslog = os.getenv('ACCESSLOG', '-')  # stdout
errorlog = os.getenv('ERRORLOG', '-')  # stdout
loglevel = os.getenv('LOGLEVEL', 'info')
