import flask
from bson.objectid import ObjectId
import bson.json_util

app = flask.current_app
blueprint = flask.Blueprint('instance', __name__, url_prefix='/instance',
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


@blueprint.route('/<ObjectId:schema_id>/<ObjectId:document_id>')
def detail(schema_id: ObjectId, document_id: ObjectId):
    """
    View an instance of a schema
    """

    db = app.mongo.db  # type: Database
    schema = db.schemas.find_one_or_404(schema_id)
    collection = getattr(db, schema['collection'])
    instance = collection.find_one_or_404(document_id)

    return flask.render_template('instance/detail.html', instance=instance,
                                 schema=schema)


@blueprint.route('/<ObjectId:schema_id>/<ObjectId:document_id>.json')
def document(schema_id: ObjectId, document_id: ObjectId):
    """
    View an instance of a schema as a JSON document
    """

    db = app.mongo.db  # type: Database
    schema = db.schemas.find_one_or_404(schema_id)
    collection = getattr(db, schema['collection'])
    instance = collection.find_one_or_404(document_id)

    instance["$schema"] = flask.url_for('schema.document', _external=True,
                                        schema_id=str(schema['_id']))
    instance["$id"] = flask.url_for(flask.request.endpoint, _external=True,
                                    schema_id=schema_id,
                                    document_id=document_id)

    return app.response_class(
        bson.json_util.dumps(instance, **flask.request.args),
        mimetype='application/schema+json')


@blueprint.route('/<ObjectId:schema_id>/list')
def list_(schema_id: ObjectId):
    db = app.mongo.db  # type: Database
    schema = db.schemas.find_one_or_404(schema_id)

    collection = getattr(db, schema['collection'])
    documents = collection.find()
    return flask.render_template('instance/list.html', schema=schema,
                                 documents=documents)


@blueprint.route('/<ObjectId:schema_id>/create', methods={'GET', 'POST'})
def create(schema_id: ObjectId):
    """
    Create an instance according to this schema
    """
    db = app.mongo.db  # type: Database
    schema = db.schemas.find_one_or_404(schema_id)

    if flask.request.method == 'POST':
        # TODO If they add a new value, then modify the schema enum

        collection = db.get_collection(
            schema['collection'])  # type:  Collection

        # Create new document from form input
        doc = {
            #  Cast data types
            key: JSON_TO_PYTHON[schema['properties'][key]['type']](value)
            for key, value in flask.request.form.items()
            # Ignore hidden values
            if not key.startswith('_')}

        result = collection.insert_one(doc)  # type: InsertOneResult
        app.logger.info(result.acknowledged)
        flask.flash(f"Added new document '{result.inserted_id}'")

        return flask.redirect(
            flask.url_for('schema.instance', schema_id=schema['_id'],
                          document_id=result.inserted_id))

    return flask.render_template('instance/create.html', schema=schema)


@blueprint.route('/<ObjectId:schema_id>/<ObjectId:document_id>/edit')
def edit(schema_id: ObjectId, document_id: ObjectId):
    """
    Change the document for an instance of a research object schema.
    """

    db = app.mongo.db  # type: Database
    schema = db.schemas.find_one_or_404(schema_id)
    collection = getattr(db, schema['collection'])
    instance = collection.find_one_or_404(document_id)

    return flask.render_template('instance/detail.html', instance=instance,
                                 schema=schema)
