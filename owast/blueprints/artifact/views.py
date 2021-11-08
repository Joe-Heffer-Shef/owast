import datetime

import flask
import azure.storage.blob

import owast.database
import owast.utils
import owast.blob

app = flask.current_app
blueprint = flask.Blueprint('artifact', __name__, url_prefix='/artifact', template_folder='templates')
db = owast.database.get_db()


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    if flask.request.method == 'POST':
        experiment_id = flask.request.form['experiment_id']

        # Add artifact record
        artifact = dict(
            experiment_id=experiment_id,
            meta=owast.utils.get_metadata(),
        )

        db.artifacts.insert_one(artifact)

        # Upload file
        for name, file in flask.request.files.items():
            blob_client = owast.blob.get_blob_client()

        # Go back to this experiment
        return flask.redirect(flask.url_for('experiment.detail', experiment_id=experiment_id))

    time = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    return flask.render_template('artifact/create.html', experiment_id=flask.request.args['experiment_id'], time=time)
