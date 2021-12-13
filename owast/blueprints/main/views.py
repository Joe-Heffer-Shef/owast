import json
import bson.json_util
from bson.objectid import ObjectId
from flask_pymongo.wrappers import Database

import flask

blueprint = flask.Blueprint('main', __name__, template_folder='templates')

app = flask.current_app


@blueprint.route('/')
def home():
    return flask.render_template('main/home.html')


@blueprint.route('/search', methods={'GET', 'POST'})
def search():
    db = app.mongo.db  # type: Database

    selected_collection = flask.request.args.get('collection')
    query = flask.request.args.get('query', '{}')
    results = tuple()
    selected_schema = None

    collections = {schema['title']: schema['collection']
                   for schema in db.schemas.find()}

    # Run query
    if selected_collection:
        collection = getattr(app.mongo.db, selected_collection)
        results = collection.find(json.loads(query))
        results = (bson.json_util.dumps(
            {k: v for k, v in obj.items() if not k.startswith('_')}
        ) for obj in results)
        selected_schema = db.schemas.find_one_or_404(
            dict(collection=selected_collection))

    return flask.render_template(
        template_name_or_list='main/search.html',
        collections=collections,
        selected_collection=selected_collection,
        query=query,
        results=results,
        selected_schema=selected_schema,
    )
