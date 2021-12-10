from typing import Mapping

import flask
import flask_wtf
from pymongo.results import InsertOneResult
from flask_pymongo.wrappers import Collection, Database

from bson.objectid import ObjectId

import owast.blueprints.relation.forms.used

app = flask.current_app
blueprint = flask.Blueprint('relation', __name__, url_prefix='/relation',
                            template_folder='templates')

# Influence map
# https://www.w3.org/TR/prov-dm/#concept-influence
# Which relations should be used to connect each type?
# https://www.w3.org/TR/prov-dm/#prov-dm-types-and-relations
# Mapping[FromType[ToType][Relation]]
PROV_RELATION = dict(
    Activity=dict(
        Activity='wasInformedBy',
        Entity='used',
        Agent='wasAssociatedWith',
    ),
    Entity=dict(
        Activity='wasGeneratedBy',
        Entity='wasDerivedFrom',
        Agent='wasAttributedTo',
    ),
    Agent=dict(
        # https://www.w3.org/TR/prov-dm/#concept-delegation
        Agent='actedOnBehalfOf',
    ),
)  # type: Mapping[str, Mapping[str, str]]

# generic relation between any two types
DEFAULT_RELATION = 'wasInfluencedBy'

RELATION_FORMS = dict(
    used=owast.blueprints.relation.forms.used.UsedForm,
)
DEFAULT_FORM = owast.blueprints.relation.forms.WasInfluencedByForm


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    """
    Create a new relation between two documents e.g. Used, WasGeneratedBy, etc.

    The relation goes from the first object to the second one, going back along
    pointing at second object as the provenance of the first object. The
    direction of the relation is "back in time" to from an item to the item
    that influenced it.

    The type of the relation is determined by the PROV type of the from and to
    instances.

    ToInstance <- Relation <- FromInstance
    """
    db = app.mongo.db  # type: Database
    schemas = db.schemas  # type: Collection

    # Build document
    # TODO additional params (metadata for relationship)
    relation = dict(
        type=str(),
        # From
        influencee_schema_id=ObjectId(
            flask.request.args['influencee_schema_id']),
        influencee_id=ObjectId(flask.request.args['influencee_id']),
    )

    # Get "From" object
    influencee_schema = schemas.find_one_or_404(
        relation['influencee_schema_id'])
    influencee_collection = getattr(db, influencee_schema[
        'collection'])  # type:Collection
    from_doc = influencee_collection.find_one_or_404(relation['influencee_id'])

    # Get "To" object
    # "To" schema
    try:
        relation['influencer_schema_id'] = ObjectId(
            flask.request.args['influencer_schema_id'])
        influencer_schema = schemas.find_one_or_404(
            relation['influencer_schema_id'])
        influencer_collection = getattr(db, influencer_schema[
            'collection'])  # type:Collection
        instances = influencer_collection.find()
    except KeyError:
        influencer_schema = dict()
        influencer_collection = None
        instances = list()

    # "To" document
    try:
        relation['influencer_id'] = ObjectId(
            flask.request.args['influencer_id'])
        influencer = influencer_collection.find_one_or_404(
            relation['influencer_id'])
    except KeyError:
        influencer = None

    # Get relation type (determined by from-schema and to-schema)
    try:
        relation['type'] = PROV_RELATION[influencee_schema['prov_type']].get(
            influencer_schema['prov_type'], DEFAULT_RELATION)
    except KeyError:
        pass

    form_class = RELATION_FORMS.get(relation['type'], DEFAULT_FORM)
    form = form_class(**relation)

    # Process form submission
    if form.validate_on_submit():
        relations = db.relations  # type: Collection
        result = relations.insert_one(relation)  # type: InsertOneResult
        app.logger.info(result.acknowledged)
        app.logger.info(f"Created relations id {result.inserted_id}")

    instances = (
        (obj['_id'], {k: v for k, v in obj.items()
                      if not k.startswith('_') and v})
        for obj in instances)

    return flask.render_template(
        template_name_or_list='relation/create.html', relation=relation,
        influencee_schema=influencee_schema, from_doc=from_doc,
        influencer_schema=influencer_schema,
        influencer=influencer, research_objects=schemas.find(),
        instances=instances, form=form)
