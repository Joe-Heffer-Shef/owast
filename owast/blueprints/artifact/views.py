"""
Artifact views
"""

import json

import flask
from bson.objectid import ObjectId
import bson.json_util
import azure.storage.blob
import azure.core.exceptions
from azure.storage.blob import ContainerClient
from pymongo.results import InsertOneResult, DeleteResult
from flask_pymongo.wrappers import Database, Collection
from werkzeug.datastructures import FileStorage

import owast.utils
import owast.blob
from .forms import ArtifactForm

app = flask.current_app
blueprint = flask.Blueprint('artifact', __name__, url_prefix='/artifact',
                            template_folder='templates')


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    """
    Add a new artifact to an experiment
    """

    try:
        experiment_id = flask.request.args['experiment_id']
    except KeyError:
        experiment_id = flask.request.form['experiment_id']
    experiment_id = ObjectId(experiment_id)

    form = ArtifactForm(experiment_id=experiment_id)

    # TODO create SAS token for Azure Blob Storage
    # this will be passed to Javascript for temporary authentication

    # TODO File upload
    # https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-nodejs

    # Uploading Large Files in Windows Azure Blob Storage Using Shared Access Signature, HTML, and JavaScript
    # https://docs.microsoft.com/en-us/answers/questions/535512/how-to-upload-large-files-in-chunks-in-azure-blobs.html

    # Process form submission
    if form.validate_on_submit():
        db = app.mongo.db  # type: Database

        # Get Azure Blob Storage service client
        service_client = owast.blob.get_service_client()
        container = str(experiment_id)

        # Upload file
        file = flask.request.files['file']  # type: FileStorage
        try:
            # Create container (a folder for the experiment)
            client = service_client.create_container(
                container)  # type: ContainerClient
            app.logger.info(f'Created container "{client.container_name}"')
        # Ignore if container already exists
        except azure.core.exceptions.ResourceExistsError:
            pass

        # TODO Use a transaction so problems are rolled back

        # Create blob
        blob_client = service_client.get_blob_client(
            container=container, blob=file.filename)
        blob_client.upload_blob(file, overwrite=True)
        flask.flash(f'Uploaded "{file.filename}"')

        influencer_collection = 'experiments'
        influencer_schema = db.schemas.find_one_or_404(dict(
            collection=influencer_collection))

        # Add artifact record
        artifact = dict(
            experiment_id=experiment_id,
            container=container,
            name=file.filename,
            **json.loads(flask.request.form['attributes']),
            relations=[
                # Add relation record
                # https://www.w3.org/TR/prov-o/#wasGeneratedBy
                dict(
                    super='wasInfluencedBy',
                    type='wasGeneratedBy',
                    influencer_id=experiment_id,
                    influencer_collection=influencer_collection,
                    influencer_schema_id=influencer_schema['_id'],
                )
            ],
        )
        result = db.artifacts.insert_one(artifact)  # type: InsertOneResult
        app.logger.info(result.acknowledged)

        # Insert the artifact metadata into the blob metadata
        blob_client.set_blob_metadata(
            dict(artifact_id=str(result.inserted_id),
                 experiment_id=str(experiment_id))
        )

        # Go back to this experiment
        return flask.redirect(
            flask.url_for('experiment.detail', experiment_id=experiment_id))

    return flask.render_template(
        template_name_or_list='artifact/create.html',
        experiment_id=experiment_id, form=form)


@blueprint.route('/<string:artifact_id>')
def detail(artifact_id: str):
    """
    Show the info for a file
    """

    # Get artifact
    artifact = app.mongo.db.artifacts.find_one_or_404(
        dict(_id=bson.objectid.ObjectId(artifact_id)))

    # Serialise artifact to JSON
    artifact_json = app.response_class(
        bson.json_util.dumps(artifact, indent=2),
        mimetype='application/json')

    return flask.render_template('artifact/detail.html',
                                 artifact=artifact,
                                 artifact_json=artifact_json)


@blueprint.route('/<string:artifact_id>/delete')
def delete(artifact_id: str):
    """
    Remove a file
    """

    # Get artifact
    artifacts = app.mongo.db.artifacts  # type: Collection
    key = dict(_id=bson.objectid.ObjectId(artifact_id))
    artifact = artifacts.find_one_or_404(key)

    # Delete blob
    service_client = owast.blob.get_service_client()
    blob_client = service_client.get_blob_client(container=artifact[
        'experiment_id'], blob=artifact['name'])
    # Ignore if already deleted out-of-band
    try:
        blob_client.delete_blob()
    except azure.core.exceptions.ResourceNotFoundError:
        pass

    # Remove artifact
    result = artifacts.delete_one(key)  # type: DeleteResult
    app.logger.debug(result.raw_result)
    flask.flash(f'Deleted artifact "{artifact_id}"')

    # Go to experiment
    return flask.redirect(
        flask.url_for('experiment.detail',
                      experiment_id=artifact['experiment_id']))


@blueprint.route('/<ObjectId:artifact_id>/download')
def download(artifact_id: ObjectId):
    """
    Download the artifact file from blob storage
    """

    # Get artifact
    artifacts = app.mongo.db.artifacts  # type: Collection
    artifact = artifacts.find_one_or_404(artifact_id)

    return flask.redirect(
        flask.url_for('blob.download', container=artifact['container'],
                      blob=artifact['name']))
