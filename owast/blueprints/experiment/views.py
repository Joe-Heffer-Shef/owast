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

import owast.database
import owast.utils

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
        # Get document collection
        experiments = db.experiments  # type: pymongo.collection.Collection

        experiment = dict(
            experiment_id=flask.request.form['experiment_id'],
            # Parse timestamp
            start_time=datetime.datetime.fromisoformat(flask.request.form['start_time']),
            meta=owast.utils.get_metadata(),
        )

        # Create new experiment record
        experiments.insert_one(experiment)

        flask.flash(f'Added experiment {experiment["experiment_id"]}')

        return flask.redirect(flask.url_for('experiment.detail', experiment_id=experiment['experiment_id']))

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
    index = dict(experiment_id=experiment_id)

    _experiment = db.experiments.find_one(index)

    # Not found
    if not _experiment:
        flask.flash(f'Experiment ID "{experiment_id}" not found')
        raise werkzeug.exceptions.NotFound

    # Show only certain fields
    experiment = {key: value for key, value in _experiment.items()
                  # Hide private fields
                  if not key.startswith('_')}

    # Get artifacts for this experiment
    artifacts = db.artifacts.find(index)

    return flask.render_template('experiment/detail.html', experiment=experiment, artifacts=artifacts)


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
