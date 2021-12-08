import json
import os

import bson.json_util
import flask
from bson.objectid import ObjectId
from flask_pymongo.wrappers import Collection, Database
from pymongo.results import UpdateResult, InsertOneResult, DeleteResult

from .forms import SchemaForm

app = flask.current_app
blueprint = flask.Blueprint('schema', __name__, url_prefix='/schema',
                            template_folder='templates')

JSON_FIELDS = {
    'properties',
    'required',
}


@blueprint.route('/')
def list_():
    schemas = app.mongo.db.schemas.find()
    return flask.render_template('schema/list.html', schemas=schemas)


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    """
    Add a new research object
    """

    form = SchemaForm()

    # Process form submission
    if form.validate_on_submit():
        # Prevent collection name conflict
        if flask.request.form['collection'] == 'schemas':
            raise ValueError('Invalid collection name')

        # Build research object from user input
        schema = dict(
            title=flask.request.form['title'],
            description=flask.request.form['description'],
            icon=flask.request.form['icon'],
            collection=flask.request.form['collection'].casefold(),
            type='object',
            properties=json.loads(flask.request.form['properties']),
            required=json.loads(flask.request.form['required']),
        )

        # Create document
        result = app.mongo.db.schemas.insert_one(
            schema)  # type: InsertOneResult

        app.logger.info(result.acknowledged)
        flask.flash(f'Created "{result.inserted_id}"')

        # Redirect to the new object
        return flask.redirect(flask.url_for('schema.detail',
                                            schema_id=result.inserted_id))

    # Show form
    return flask.render_template('schema/create.html', form=form)


@blueprint.route('/<ObjectId:schema_id>')
def detail(schema_id: ObjectId):
    schema = app.mongo.db.schemas.find_one_or_404(schema_id)
    return flask.render_template('schema/detail.html', schema=schema)


def build_json_schema_document(schema: dict) -> dict:
    uri = flask.url_for('schema.doc', schema_id=str(schema['_id']),
                        _external=True)
    return dict(
        **{'$schema': os.environ['JSON_SCHEMA_SPEC'],
           '$id': uri},
        **{key: value for key, value in schema.items() if
           not key.startswith('_')}
    )


@blueprint.route('/<ObjectId:schema_id>/schema.json')
def doc(schema_id: ObjectId):
    """
    Show the JSON schema document

    https://json-schema.org/draft/2020-12/json-schema-core.html
    """
    schema = app.mongo.db.schemas.find_one_or_404(schema_id)
    schema_document = build_json_schema_document(schema)
    return app.response_class(
        bson.json_util.dumps(schema_document, **flask.request.args),
        mimetype='application/schema+json')


@blueprint.route('/<ObjectId:schema_id>/delete')
def delete(schema_id: ObjectId):
    schemas = app.mongo.db.schemas  # type: Collection
    result = schemas.delete_one(
        dict(_id=schema_id))  # type: DeleteResult
    app.logger.info(result.raw_result)
    flask.flash(f'Deleted {schema_id}')
    return flask.redirect(flask.url_for('schema.list_'))


@blueprint.route('/<ObjectId:schema_id>/edit', methods={'GET', 'POST'})
def edit(schema_id: ObjectId):
    """
    Modify a research object
    """

    collection = app.mongo.db.schemas  # type: Collection
    schema = collection.find_one_or_404(schema_id)

    form = SchemaForm()

    # Process form submission
    if form.validate_on_submit():
        # Parse JSON fields
        _schema = {key: json.loads(value) if key in JSON_FIELDS else value
                   for key, value in form.data.items()}
        # Write changes to database
        result = collection.update_one(
            dict(_id=schema_id), {'$set': _schema})  # type: UpdateResult
        app.logger.info(result.raw_result)
        flask.flash(f"Saved changes to '{schema['title']}'")
        return flask.redirect(flask.url_for('schema.detail',
                                            schema_id=schema_id))

    # Convert fields to JSON
    form.process(
        **{key: json.dumps(schema[key]) if key in JSON_FIELDS else value for
           key, value in schema.items()})
    return flask.render_template('schema/edit.html', schema=schema, form=form)
