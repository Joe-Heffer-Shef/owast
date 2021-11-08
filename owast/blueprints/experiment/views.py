"""
Experiment views
"""

import datetime

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


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    """
    Write new experiment metadata and file upload.
    """

    if flask.request.method == 'POST':
        experiment = dict(flask.request.form)
        experiment['start_time'] = datetime.datetime.fromisoformat(experiment['start_time'])

        # Get document collection
        experiments = db.experiments  # type: pymongo.collection.Collection

        # Create new experiment record
        experiments.insert_one(experiment)

        flask.flash(f'Added experiment {experiment}')

        return flask.redirect(flask.url_for('experiment.list_'))

    return flask.render_template('experiment/create.html')


@blueprint.route('/<string:experiment_id>')
def detail(experiment_id: str):
    """
    Show the details of a particular experiment
    """

    experiment = db.experiment.find_one(dict(experiment_id=experiment_id))

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
