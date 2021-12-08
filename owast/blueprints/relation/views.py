import flask
from pymongo.results import InsertOneResult
from flask_pymongo.wrappers import Collection

from bson.objectid import ObjectId

app = flask.current_app
blueprint = flask.Blueprint('relation', __name__, url_prefix='/relation',
                            template_folder='templates')


@blueprint.route('/create')
def create():
    """
    Create a new relation between two documents e.g. Used, WasGeneratedBy, etc.

    The relation goes from the first object to the second one, going back along
    pointing at second object as the provenance of the first object.
    """

    # Build document
    # TODO additional params
    relation = dict(
        # From
        from_schema_id=ObjectId(flask.request.args['from_schema_id']),
        from_document_id=ObjectId(flask.request.args['from_document_id']),

        # To
        to_schema_id=ObjectId(flask.request.args['to_schema_id']),
        to_document_id=ObjectId(flask.request.args['to_document_id']),
    )

    relations = app.mongo.db.relations  # type: Collection
    result = relations.insert_one(relation)  # type: InsertOneResult
    app.logger.info(result.acknowledged)
    app.logger.info(f"Created relations id {result.inserted_id}")
