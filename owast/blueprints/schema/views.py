import json
import os

import flask
import pymongo.results
import pymongo.database
import pymongo.collection
import flask_pymongo.wrappers
from bson.objectid import ObjectId
import bson.json_util

app = flask.current_app
blueprint = flask.Blueprint('schema', __name__, url_prefix='/schema',
                            template_folder='templates')

# Map JSON Schema data types to Python native types
# https://json-schema.org/understanding-json-schema/reference/type.html
JSON_TO_PYTHON = dict(
    string=str,
    integer=int,
    boolean=bool,
    number=float,
    object=dict,
    array=list,
    null=None,
)


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
            schema)  # type:pymongo.results.InsertOneResult

        app.logger.info(result.acknowledged)
        flask.flash(f'Created "{result.inserted_id}"')

        # Redirect to the new object
        return flask.redirect(flask.url_for('schema.detail',
                                            schema_id=result.inserted_id))

    # Show form
    return flask.render_template('schema/create.html')


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
    schemas = app.mongo.db.schemas  # type: flask_pymongo.wrappers.Collection
    result = schemas.delete_one(
        dict(_id=schema_id))  # type: pymongo.results.DeleteResult
    app.logger.info(result.raw_result)
    flask.flash(f'Deleted {schema_id}')
    return flask.redirect(flask.url_for('schema.list_'))


@blueprint.route('/<ObjectId:schema_id>/add', methods={'GET', 'POST'})
def add(schema_id: ObjectId):
    """
    Create an instance according to this schema
    """
    db = app.mongo.db  # type: pymongo.database.Database
    schema = db.schemas.find_one_or_404(schema_id)

    if flask.request.method == 'POST':
        # TODO If they add a new value, then modify the schema enum

        collection = db.get_collection(
            schema['collection'])  # type:  flask_pymongo.wrappers.Collection

        # Create new document from form input
        document = {
            #  Cast data types
            key: JSON_TO_PYTHON[schema['properties'][key]['type']](value)
            for key, value in flask.request.form.items()
            # Ignore hidden values
            if not key.startswith('_')}

        result = collection.insert_one(
            document)  # type: pymongo.results.InsertOneResult
        app.logger.info(result.acknowledged)
        flask.flash(f"Added new document '{result.inserted_id}'")

        return flask.redirect(
            flask.url_for('schema.instance', schema_id=schema['_id'],
                          document_id=result.inserted_id))

    return flask.render_template('schema/add.html', schema=schema)


@blueprint.route('/<ObjectId:schema_id>/<ObjectId:document_id>')
def instance(schema_id: ObjectId, document_id: ObjectId):
    """
    View an instance of a schema
    """
    db = app.mongo.db  # type: flask_pymongo.wrappers.Database
    schema = db.schemas.find_one_or_404(schema_id)
    collection = getattr(db, schema['collection'])
    document = collection.find_one_or_404(document_id)

    return flask.render_template('schema/instance.html', document=document,
                                 schema=schema)


@blueprint.route('/<ObjectId:schema_id>/<ObjectId:document_id>.json')
def instance_doc(schema_id: ObjectId, document_id: ObjectId):
    """
    View an instance of a schema as a JSON document
    """
    db = app.mongo.db  # type: flask_pymongo.wrappers.Database
    schema = db.schemas.find_one_or_404(schema_id)
    collection = getattr(db, schema['collection'])
    document = collection.find_one_or_404(document_id)

    document["$schema"] = os.environ['JSON_SCHEMA_SPEC']
    document["$id"] = flask.url_for(flask.request.endpoint, _external=True,
                                    schema_id=schema_id,
                                    document_id=document_id)

    return app.response_class(
        bson.json_util.dumps(document, **flask.request.args),
        mimetype='application/schema+json')


@blueprint.route('/<ObjectId:schema_id>/list')
def instances(schema_id: ObjectId):
    db = app.mongo.db  # type: flask_pymongo.wrappers.Database
    schema = db.schemas.find_one_or_404(schema_id)
    collection = getattr(db, schema['collection'])
    documents = collection.find()
    return flask.render_template('schema/instances.html', schema=schema,
                                 documents=documents)
