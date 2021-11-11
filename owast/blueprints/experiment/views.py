"""
Experiment views
"""

import datetime
import uuid

import werkzeug.exceptions
import flask
import pymongo.database
import pymongo.collection
import pymongo.results
import azure.storage.blob

import owast.database
import owast.utils
import owast.blob

app = flask.current_app
blueprint = flask.Blueprint('experiment', __name__, url_prefix='/experiment',
                            template_folder='templates')
db = owast.database.get_db()


@blueprint.route('/')
def list_():
    experiments = db.experiments.find()
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

        # Create container
        service_client = owast.blob.get_service_client()
        container_client = service_client.create_container(
            container)  # type: azure.storage.blob.ContainerClient
        container_client.set_container_metadata(
            dict(experiment_id=experiment_id))

        # Get document collection
        experiments = db.experiments  # type: pymongo.collection.Collection

        # Create new experiment record
        experiment = dict(
            experiment_id=experiment_id,
            # Parse timestamp
            start_time=datetime.datetime.fromisoformat(
                flask.request.form['start_time']),
            meta=owast.utils.get_metadata(),
            container=container,
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

    _experiment = db.experiments.find_one(index)

    # Not found
    if not _experiment:
        app.logger.warning(f'Experiment ID "{experiment_id}" not found')
        raise werkzeug.exceptions.NotFound

    # Show only certain fields
    experiment = {key: value for key, value in _experiment.items()
                  # Hide private fields
                  if not key.startswith('_')}

    # Get artifacts for this experiment
    artifacts = db.artifacts.find(index)

    return flask.render_template('experiment/detail.html',
                                 experiment=experiment, artifacts=artifacts)


@blueprint.route('/<string:experiment_id>/delete')
def delete(experiment_id: str):
    """
    Remove an experiment document
    """

    # Get the experiment record
    key = dict(experiment_id=experiment_id)
    experiments = db.experiments  # type: pymongo.collection.Collection
    experiment = experiments.find_one(key)

    # Remove the container
    service_client = owast.blob.get_service_client()
    service_client.delete_container(experiment['container'])

    # Remove experiment record
    result = experiments.delete_one(
        experiment)  # type: pymongo.results.DeleteResult

    app.logger.info(result.raw_result)

    flask.flash(f'Deleted experiment "{experiment_id}"')

    return flask.redirect(flask.url_for('experiment.list_'))
