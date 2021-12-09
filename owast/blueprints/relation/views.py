from typing import List

import flask
from pymongo.results import InsertOneResult
from flask_pymongo.wrappers import Collection, Database

from bson.objectid import ObjectId

app = flask.current_app
blueprint = flask.Blueprint('relation', __name__, url_prefix='/relation',
                            template_folder='templates')


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    """
    Create a new relation between two documents e.g. Used, WasGeneratedBy, etc.

    The relation goes from the first object to the second one, going back along
    pointing at second object as the provenance of the first object.
    """
    db = app.mongo.db  # type: Database
    schemas = db.schemas  # type: Collection

    # Build document
    # TODO additional params (metadata for relationship)
    relation = dict(
        # From
        from_schema_id=ObjectId(flask.request.args['from_schema_id']),
        from_document_id=ObjectId(flask.request.args['from_document_id']),
    )

    # To
    try:
        relation['to_schema_id'] = ObjectId(flask.request.args['to_schema_id'])
        to_schema = schemas.find_one_or_404(relation['to_schema_id'])
        to_collection = getattr(db, to_schema['collection'])  # type:Collection
    except KeyError:
        to_schema = None
    try:
        relation['to_document_id'] = ObjectId(
            flask.request.args['to_document_id'])

        to_doc = to_collection.find_one_or_404(relation['to_document_id'])
    except KeyError:
        to_doc = None

    # Get "From" object
    from_schema = schemas.find_one_or_404(relation['from_schema_id'])
    from_collection = getattr(db, from_schema['collection'])  # type:Collection
    from_doc = from_collection.find_one_or_404(relation['from_document_id'])

    if flask.request.method == 'POST':
        relations = db.relations  # type: Collection
        result = relations.insert_one(relation)  # type: InsertOneResult
        app.logger.info(result.acknowledged)
        app.logger.info(f"Created relations id {result.inserted_id}")

    return flask.render_template(
        template_name_or_list='relation/create.html', relation=relation,
        from_schema=from_schema, from_doc=from_doc, to_schema=to_schema,
        to_doc=to_doc, research_objects=schemas.find(),
        instances=to_collection.find())
