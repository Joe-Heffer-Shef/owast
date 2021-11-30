import json

import flask
import pymongo.results
from bson.objectid import ObjectId
import bson.json_util

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
    """
    Add a new research object
    """
    # Process form submisson
    if flask.request.method == 'POST':
        # Build research object from user input
        thing = {
            'title': '',
            'description': '',
            'type': 'object',
        }
        thing.update(json.loads(flask.request.form['_schema']))
        thing.update({k: v for k, v in flask.request.form.items() if
                      not k.startswith('_')})

        # Create document
        result = app.mongo.db.things.insert_one(
            thing)  # type:pymongo.results.InsertOneResult

        app.logger.info(result.acknowledged)
        flask.flash(f'Created "{result.inserted_id}"')

        # Redirect to the new obhect
        return flask.redirect(flask.url_for('thing.detail',
                                            thing_id=result.inserted_id))

    # Show form
    return flask.render_template('thing/create.html')


@blueprint.route('/<ObjectId:thing_id>')
def detail(thing_id: ObjectId):
    thing = app.mongo.db.things.find_one_or_404(thing_id)
    return flask.render_template('thing/detail.html', thing=thing)


@blueprint.route('/<ObjectId:thing_id>/schema.json')
def schema(thing_id: ObjectId):
    """
    Show the JSON schema document
    """
    thing = app.mongo.db.things.find_one_or_404(thing_id)
    schema = dict(
        **{
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            '$id': f'https://localhost/thing/{thing_id}/schema.json',
        },
        **{key: value for key, value in thing.items() if
           not key.startswith('_')}
    )
    return app.response_class(
        bson.json_util.dumps(schema, **flask.request.args),
        mimetype='application/json')


@blueprint.route('/<ObjectId:thing_id>/delete')
def delete(thing_id: ObjectId):
    things = app.mongo.db.things  # type: flask_pymongo.wrappers.Collection
    result = things.delete_one(
        dict(_id=thing_id))  # type: pymongo.results.DeleteResult
    app.logger.info(result.raw_result)
    flask.flash(f'Deleted {thing_id}')
    return flask.redirect(flask.url_for('thing.list_'))
