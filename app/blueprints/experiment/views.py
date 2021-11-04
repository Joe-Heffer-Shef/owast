import flask

blueprint = flask.Blueprint('experiment', __name__)


@blueprint.route('/create')
def create():
    """
    Write new experiment metadata and file upload.
    """

    # TODO create SAS token for Azure Blob Storage
    # this will be passed to Javascript for temporary authentication

    # TODO File upload
    # https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-nodejs

    # Uploading Large Files in Windows Azure Blob Storage Using Shared Access Signature, HTML, and JavaScript
    # https://docs.microsoft.com/en-us/answers/questions/535512/how-to-upload-large-files-in-chunks-in-azure-blobs.html

    return flask.render_template('experiment/create.html')
