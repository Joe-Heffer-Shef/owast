import json

import flask
from bson.objectid import ObjectId
from flask_pymongo.wrappers import Collection, Database
from pymongo.results import InsertOneResult
from types import SimpleNamespace

import owast.blueprints.relation.forms.used
from owast.blueprints.relation.constants import PROV_RELATION, DEFAULT_RELATION

app = flask.current_app
blueprint = flask.Blueprint('relation', __name__, url_prefix='/relation',
                            template_folder='templates')

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

    # Load user input (GET or POST)
    relation = {key: value for key, value in
                (flask.request.form if flask.request.method == 'POST'
                 else flask.request.args).items()
                # Ignore hidden fields such as CSRF token
                if not key.startswith('_')}
    relation.setdefault('type', DEFAULT_RELATION)

    # Initialise form widgets
    form_class = RELATION_FORMS.get(relation['type'], DEFAULT_FORM)
    form = form_class(**relation)

    # Process form submission
    if form.validate_on_submit():
        # Create new relation document from for data
        rel = SimpleNamespace(**relation)
        form.populate_obj(rel)
        rel_doc = rel.__dict__.copy()
        rel_doc.update(rel_doc.pop('attributes'))

        relations = db.relations  # type: Collection
        result = relations.insert_one(rel_doc)  # type: InsertOneResult
        app.logger.info(result.acknowledged)
        app.logger.info(f"Created relations id '{result.inserted_id}'")

        return flask.redirect(
            flask.url_for('relation.detail', relation_id=result.inserted_id))

    # Get influencee object (from)
    influencee_schema = schemas.find_one_or_404(ObjectId(
        relation['influencee_schema_id']))
    influencee_collection = getattr(db, influencee_schema[
        'collection'])  # type:Collection
    influencee = influencee_collection.find_one_or_404(ObjectId(
        relation['influencee_id']))

    # Influencer schema and collection
    try:
        influencer_schema = schemas.find_one_or_404(ObjectId(
            relation['influencer_schema_id']))
        influencer_collection = getattr(db, influencer_schema[
            'collection'])  # type:Collection
        instances = influencer_collection.find()
    except KeyError:
        influencer_schema = dict()
        influencer_collection = None
        instances = list()

    # Influencer document
    try:
        influencer = influencer_collection.find_one_or_404(ObjectId(
            relation['influencer_id']))
    except (KeyError, AttributeError):
        influencer = None

    # Relation
    # Get relation type (determined by from-schema and to-schema)
    try:
        relation['type'] = PROV_RELATION[influencee_schema['prov_type']][
            influencer_schema['prov_type']]
    except KeyError:
        pass

    # Convert to human-readable format to display in the HTML form
    instances = ((obj['_id'], {k: v for k, v in obj.items()
                               if not k.startswith('_') and v})
                 for obj in instances if obj['_id'] != influencee['_id'])

    # Update form values
    form.process(**relation)
    return flask.render_template(
        template_name_or_list='relation/create.html', relation=relation,
        influencee_schema=influencee_schema, influencee=influencee,
        influencer_schema=influencer_schema,
        influencer=influencer, research_objects=schemas.find(),
        instances=instances, form=form)


@blueprint.route('/<ObjectId:relation_id>')
def detail(relation_id: ObjectId):
    relation = app.mongo.db.relations.find_one_or_404(relation_id)
    return flask.render_template('relation/detail.html', relation=relation)
