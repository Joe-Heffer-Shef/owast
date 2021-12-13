import itertools
from typing import Tuple

import bson.json_util
import flask
import graphviz
from bson.objectid import ObjectId
from flask_pymongo.wrappers import Database, Collection

app = flask.current_app
blueprint = flask.Blueprint('instance', __name__, url_prefix='/instance',
                            template_folder='templates')

ObjectId.generation_time

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


def get_instance(schema_id: ObjectId, document_id: ObjectId) -> Tuple[dict,
                                                                      dict]:
    db = app.mongo.db  # type: Database
    schema = db.schemas.find_one_or_404(schema_id)
    collection = getattr(db, schema['collection'])
    instance = collection.find_one_or_404(document_id)

    return schema, instance


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


def add_node(graph: graphviz.Digraph, schema: dict, instance: dict) -> \
        graphviz.Digraph:
    db = app.mongo.db  # type: Database

    label = schema['title'] + '\n' + '\n'.join(itertools.islice(
        (f"{k}: {v}" for k, v in instance.items() if not k.startswith('_')
         and v), 0, 3))
    graph.node(str(instance['_id']), label=label)

    # Iterate over relationships
    relations = db.relations.find(dict(influencee_id=instance['_id']))
    for relation in relations:
        influencer_schema = db.schemas.find_one_or_404(
            relation['influencer_schema_id'])
        influencer_collection = getattr(db, influencer_schema[
            'collection'])  # type: Collection
        influencer = influencer_collection.find_one_or_404(
            relation['influencer_id'])

        # Connect the nodes
        graph.edge(str(instance['_id']), str(influencer['_id']),
                   label=str(relation['type']))

        add_node(graph, schema=influencer_schema, instance=influencer)

    return graph


def build_graph(schema: dict, instance: dict) -> graphviz.Digraph:
    graph = graphviz.Digraph(str(instance['_id']),
                             comment=schema['collection'])

    # Recursively add nodes
    add_node(graph, schema, instance)

    return graph


@blueprint.route('/<ObjectId:schema_id>/<ObjectId:document_id>.dot')
def dot(schema_id: ObjectId, document_id: ObjectId):
    """
    GraphViz DOT notation

    https://www.graphviz.org/doc/info/lang.html
    """
    schema, instance = get_instance(schema_id, document_id)

    graph = build_graph(schema=schema, instance=instance)

    return app.response_class(graph.source, mimetype='text/vnd.graphviz')


@blueprint.route('/<ObjectId:schema_id>/<ObjectId:document_id>.svg')
def dot_image(schema_id: ObjectId, document_id: ObjectId):
    """
    Render network graph as a vector image
    """
    schema, instance = get_instance(schema_id, document_id)

    graph = build_graph(schema=schema, instance=instance)

    return app.response_class(graph.pipe(format='svg'),
                              mimetype='image/svg+xml')
