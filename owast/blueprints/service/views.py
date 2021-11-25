import os

import flask
import pymongo.errors

app = flask.current_app
blueprint = flask.Blueprint('service', __name__, url_prefix='/service',
                            template_folder='templates')


def ping_mongodb(timeout: int = 1000, host=None,
                 **mongo_client_kwargs):
    """
    Is MongoDB up?
    """
    try:
        with pymongo.MongoClient(host or os.environ['MONGO_URI'],
                                 serverSelectionTimeoutMS=timeout,
                                 **mongo_client_kwargs) as client:
            return client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as exc:
        return exc


def ping_blob():
    return


@blueprint.route('/')
def list_():
    services = list()

    services.append(dict(name='NoSQL database', status=ping_mongodb()))
    services.append(dict(name='Blob storage', status=ping_blob()))

    return flask.render_template('service/list.html', services=services)
