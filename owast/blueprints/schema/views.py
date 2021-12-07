import json

import flask
import pymongo.results
from bson.objectid import ObjectId
import bson.json_util

app = flask.current_app
blueprint = flask.Blueprint('schema', __name__, url_prefix='/schema',
                            template_folder='templates')


@blueprint.route('/')
def list_():
    schemas = app.mongo.db.schemas.find()
    return flask.render_template('schema/list.html', schemas=schemas)


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    """
    Add a new research object
    """

    # Process form submission
    if flask.request.method == 'POST':
        # Build research object from user input
        schema = dict(
            title=flask.request.form['title'],
            description=flask.request.form['description'],
            type='object',
            properties=json.loads(flask.request.form['properties']),
            required=json.loads(flask.request.form['required']),
        )

        # Create document
        result = app.mongo.db.schemas.insert_one(
            schema)  # type:pymongo.results.InsertOneResult

        app.logger.info(result.acknowledged)
        flask.flash(f'Created "{result.inserted_id}"')

        # Redirect to the new obhect
        return flask.redirect(flask.url_for('schema.detail',
                                            schema_id=result.inserted_id))

    # Show form
    return flask.render_template('schema/create.html')


@blueprint.route('/<ObjectId:schema_id>')
def detail(schema_id: ObjectId):
    schema = app.mongo.db.schemas.find_one_or_404(schema_id)
    return flask.render_template('schema/detail.html', schema=schema)


@blueprint.route('/<ObjectId:schema_id>/schema.json')
def doc(schema_id: ObjectId):
    """
    Show the JSON schema document

    https://json-schema.org/draft/2020-12/json-schema-core.html
    """
    _schema = app.mongo.db.schemas.find_one_or_404(schema_id)
    # Build schema document
    schema = dict(
        **{
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            '$id': f'https://localhost/schema/{schema_id}/schema.json',
        },
        **{key: value for key, value in _schema.items() if
           not key.startswith('_')}
    )
    return app.response_class(
        bson.json_util.dumps(schema, **flask.request.args),
        mimetype='application/schema+json')


@blueprint.route('/<ObjectId:schema_id>/delete')
def delete(schema_id: ObjectId):
    schemas = app.mongo.db.schemas  # type: flask_pymongo.wrappers.Collection
    result = schemas.delete_one(
        dict(_id=schema_id))  # type: pymongo.results.DeleteResult
    app.logger.info(result.raw_result)
    flask.flash(f'Deleted {schema_id}')
    return flask.redirect(flask.url_for('schema.list_'))


@blueprint.route('/<ObjectId:schema_id>/add')
def add(schema_id: ObjectId):
    """
    Create an instance according to this schema
    """
    schema = app.mongo.db.schemas.find_one_or_404(schema_id)
    return flask.render_template('schema/add.html', schema=schema)
