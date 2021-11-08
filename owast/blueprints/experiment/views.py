"""
Experiment views
"""

import datetime
import json
import uuid

import flask
import pymongo.database
import pymongo.collection
import pymongo.results

import owast.database

app = flask.current_app
blueprint = flask.Blueprint('experiment', __name__, url_prefix='/experiment', template_folder='templates')
db = owast.database.get_db()


@blueprint.route('/')
def list_():
    experiments = db.experiments.find()
    return flask.render_template('experiment/list.html', experiments=experiments)


def create_experiment() -> dict:
    """
    Initialise a new experiment record
    """

    experiment = dict(
        experiment_id=flask.request.form['experiment_id'],
        # Parse timestamp
        start_time=datetime.datetime.fromisoformat(flask.request.form['start_time']),
        meta=dict(),
    )

    # Iterate over any number of custom metadata fields
    i = 1
    while True:
        try:
            key = flask.request.form[f'meta_{i}_key']
        except KeyError:
            break
        value = flask.request.form[f'meta_{i}_value']
        experiment['meta'][key] = value
        i += 1

    return experiment


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    """
    Write new experiment metadata and file upload.
    """

    if flask.request.method == 'POST':
        # Get document collection
        experiments = db.experiments  # type: pymongo.collection.Collection

        experiment = create_experiment()

        # Create new experiment record
        experiments.insert_one(experiment)

        flask.flash(f'Added experiment {experiment}')

        return flask.redirect(flask.url_for('experiment.list_'))

    # Default to current time
    time = datetime.datetime.now().replace(microsecond=0).isoformat()

    # Default random experiment identifier
    experiment_id = str(uuid.uuid4())

    return flask.render_template('experiment/create.html', time=time, experiment_id=experiment_id)


@blueprint.route('/<string:experiment_id>')
def detail(experiment_id: str):
    """
    Show the details of a particular experiment
    """

    _experiment = db.experiment.find_one(dict(experiment_id=experiment_id))

    # Show only certain fields
    experiment = {key: value for key, value in _experiment.items() if not key.startswith('_')}

    experiment = json.dumps(experiment, indent=2)

    # TODO create SAS token for Azure Blob Storage
    # this will be passed to Javascript for temporary authentication

    # TODO File upload
    # https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-nodejs

    # Uploading Large Files in Windows Azure Blob Storage Using Shared Access Signature, HTML, and JavaScript
    # https://docs.microsoft.com/en-us/answers/questions/535512/how-to-upload-large-files-in-chunks-in-azure-blobs.html

    return flask.render_template('experiment/detail.html', experiment=experiment)


@blueprint.route('/<string:experiment_id>/delete')
def delete(experiment_id: str):
    """
    Remove an experiment document
    """

    experiment = dict(experiment_id=experiment_id)
    experiments = db.experiments  # type: pymongo.collection.Collection

    result = experiments.delete_one(experiment)  # type: pymongo.results.DeleteResult

    app.logger.info(result.raw_result)

    flask.flash(f'Deleted experiment "{experiment_id}"')

    return flask.redirect(flask.url_for('experiment.list_'))
