"""
Experiment views
"""

import datetime
import uuid

import bson
import flask
import pymongo.database
import pymongo.collection
import pymongo.results
import azure.storage.blob

import owast.utils
import owast.blob

app = flask.current_app
blueprint = flask.Blueprint('experiment', __name__, url_prefix='/experiment',
                            template_folder='templates')


@blueprint.route('/')
def list_():
    """
    Show experiments
    """
    # Get all experiments, except deleted ones
    experiments = app.mongo.db.experiments.find(dict(deleted=False))
    return flask.render_template('experiment/list.html',
                                 experiments=experiments)


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    """
    Create a new experiment record and the container associated with it.
    """

    # Process form submission
    if flask.request.method == 'POST':
        experiment_id = flask.request.form['experiment_id']
        container = experiment_id

        # TODO validate container name
        # https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata

        # Create container
        # TODO transaction

        service_client = owast.blob.get_service_client()
        container_client = service_client.create_container(
            container)  # type: azure.storage.blob.ContainerClient
        container_client.set_container_metadata(
            dict(experiment_id=experiment_id))

        # Get document collection
        experiments = app.mongo.db.experiments  # type: pymongo.collection.Collection

        # Create new experiment record
        experiment = dict(
            experiment_id=experiment_id,
            # Parse timestamp
            start_time=datetime.datetime.fromisoformat(
                flask.request.form['start_time']),
            meta=owast.utils.get_metadata(),
            container=container,
            deleted=False,
        )
        experiments.insert_one(experiment)

        flask.flash(f'Added experiment {experiment_id}')

        return flask.redirect(flask.url_for('experiment.detail',
                                            experiment_id=experiment[
                                                'experiment_id']))

    # Create default values for form fields
    time = owast.utils.html_datetime()
    # Default random experiment identifier
    experiment_id = str(uuid.uuid4())

    return flask.render_template('experiment/create.html',
                                 time=time, experiment_id=experiment_id)


@blueprint.route('/<string:experiment_id>')
def detail(experiment_id: str):
    """
    Show the details of a particular experiment
    """
    index = dict(experiment_id=experiment_id)

    _experiment = app.mongo.db.experiments.find_one_or_404(index)

    # Show only certain fields
    experiment = {key: value for key, value in _experiment.items()
                  # Hide private fields
                  if not key.startswith('_')}

    # Get artifacts for this experiment
    artifacts = app.mongo.db.artifacts.find(index)

    return flask.render_template('experiment/detail.html',
                                 experiment=experiment, artifacts=artifacts)


@blueprint.route('/<string:experiment_id>/delete')
def delete(experiment_id: str):
    """
    Delete an experiment i.e. set deleted attribute to true.
    """

    key = dict(experiment_id=experiment_id)
    experiments = app.mongo.db.experiments  # type: pymongo.collection.Collection
    update_result = experiments.update_one(key, {
        '$set': dict(deleted=True)})  # type: pymongo.results.UpdateResult
    app.logger.debug(update_result.raw_result)

    flask.flash(f'Deleted experiment "{experiment_id}"')

    return flask.redirect(flask.url_for('experiment.list_'))
