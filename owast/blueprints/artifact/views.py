import datetime

import flask
import bson.objectid
import bson.json_util
import werkzeug.exceptions
import azure.storage.blob
import azure.core.exceptions
import pymongo.collection
import pymongo.results

import owast.database
import owast.utils
import owast.blob

app = flask.current_app
blueprint = flask.Blueprint('artifact', __name__, url_prefix='/artifact',
                            template_folder='templates')
db = owast.database.get_db()


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    # TODO create SAS token for Azure Blob Storage
    # this will be passed to Javascript for temporary authentication

    # TODO File upload
    # https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-nodejs

    # Uploading Large Files in Windows Azure Blob Storage Using Shared Access Signature, HTML, and JavaScript
    # https://docs.microsoft.com/en-us/answers/questions/535512/how-to-upload-large-files-in-chunks-in-azure-blobs.html

    if flask.request.method == 'POST':
        experiment_id = flask.request.form['experiment_id']
        container = experiment_id

        # Get Azure Blob Storage service client
        service_client = owast.blob.get_service_client()

        # Upload file
        for name, file in flask.request.files.items():
            try:
                # Create container (a folder for the experiment)
                container_result = service_client.create_container(container)
                app.logger.debug(container_result)
            # Ignore if container already exists
            except azure.core.exceptions.ResourceExistsError:
                pass

            # Create blob
            blob_client = service_client.get_blob_client(
                container=experiment_id, blob=file.filename)
            blob_result = blob_client.upload_blob(file, overwrite=True)

            app.logger.debug(blob_result)

            flask.flash(f'Uploaded "{file.filename}"')

            # Add artifact record
            artifact = dict(
                experiment_id=experiment_id,
                container=container,
                meta=owast.utils.get_metadata(),
                name=file.filename,
                blob=blob_result.copy(),
            )
            # Encode MD5-sum as a string
            artifact['blob']['content_md5'] = artifact['blob'][
                'content_md5'].hex()

            app.logger.info(artifact)
            db.artifacts.insert_one(artifact)

        # Go back to this experiment
        return flask.redirect(
            flask.url_for('experiment.detail', experiment_id=experiment_id))

    time = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    return flask.render_template('artifact/create.html',
                                 experiment_id=flask.request.args[
                                     'experiment_id'], time=time)


@blueprint.route('/<string:artifact_id>')
def detail(artifact_id: str):
    """
    Show the info for a file
    """

    # Get artifact
    artifact = db.artifacts.find_one(
        dict(_id=bson.objectid.ObjectId(artifact_id)))
    if not artifact:
        raise werkzeug.exceptions.NotFound

    # Serialise artifact to JSON
    artifact_json = app.response_class(
        bson.json_util.dumps(artifact, indent=2),
        mimetype='application/json')

    # Get blob
    service_client = owast.blob.get_service_client()
    app.logger.info(artifact['blob'])
    blob_client = service_client.get_blob_client(
        container=artifact['container'], blob=artifact['blob']['name'])
    blob = blob_client.get_blob_properties()

    return flask.render_template('artifact/detail.html',
                                 artifact=artifact_json, blob=blob)


@blueprint.route('/<string:artifact_id>/delete')
def delete(artifact_id: str):
    """
    Remove a file
    """
    artifacts = db.artifacts  # type: pymongo.collection.Collection

    key = dict(_id=bson.objectid.ObjectId(artifact_id))

    # Get artifact
    artifact = artifacts.find_one(key)

    # Delete blob
    service_client = owast.blob.get_service_client()
    blob_client = service_client.get_blob_client(container=artifact[
        'experiment_id'], blob=artifact['name'])
    blob_client.delete_blob()

    # Remove artifact
    result = artifacts.delete_one(key)  # type: pymongo.results.DeleteResult
    app.logger.debug(result.raw_result)
    flask.flash(f'Deleted artifact "{artifact_id}"')

    return flask.redirect(flask.url_for('experiment.list_'))
