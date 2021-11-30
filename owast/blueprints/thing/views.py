import json

import flask
import pymongo.results
from bson.objectid import ObjectId

app = flask.current_app
blueprint = flask.Blueprint('thing', __name__,
                            url_prefix='/thing',
                            template_folder='templates')


@blueprint.route('/')
def list_():
    things = app.mongo.db.things.find()
    return flask.render_template('thing/list.html',
                                 things=things)


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    if flask.request.method == 'POST':
        thing = {
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            '$id': 'https://localhost/thing/{thing_id}/schema.json',
            'title': '',
            'description': '',
            'type': 'object',
        }
        _thing = json.loads(flask.request.form['schema'])
        thing.update(flask.request.form)
        result = app.mongo.db.things.insert_one(
            thing)  # type:pymongo.results.InsertOneResult
        app.logger.info(result.acknowledged)
        flask.flash(f'Created "{result.inserted_id}"')
        return flask.redirect(flask.url_for('thing.detail',
                                            thing_id=result.inserted_id))

    return flask.render_template('thing/create.html')


@blueprint.route('/<ObjectId:thing_id>')
def detail(thing_id: ObjectId):
    thing = app.mongo.db.things.find_one_or_404(thing_id)
    return flask.render_template('thing/detail.html', thing=thing)


@blueprint.route('/<ObjectId:thing_id>/schema.json')
def detail_json(thing_id: ObjectId):
    thing = app.mongo.db.things.find_one_or_404(thing_id)
    return flask.jsonify(thing)
