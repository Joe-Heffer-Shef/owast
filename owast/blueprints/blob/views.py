import io

import flask

import owast.blob

app = flask.current_app
blueprint = flask.Blueprint('blob', __name__, url_prefix='/blob',
                            template_folder='templates')
service_client = owast.blob.get_service_client()


def iter_blobs():
    for container in service_client.list_containers():
        container_client = service_client.get_container_client(container)
        yield from container_client.list_blobs()


@blueprint.route('/')
def list_():
    """
    Show all blobs
    """

    return flask.render_template('blob/list.html', blobs=iter_blobs())


@blueprint.route('/<string:container>/<string:blob>')
def detail(container: str, blob: str):
    """
    Inspect a single blob
    """
    blob_client = service_client.get_blob_client(
        container=container, blob=blob)

    blob = blob_client.get_blob_properties()

    return flask.render_template('blob/detail.html', blob=blob)


@blueprint.route('/<string:container>/<string:blob>/download')
def download(container: str, blob: str):
    """
    Retrieve data for this file
    """
    # Download blob
    blob_client = service_client.get_blob_client(
        container=container, blob=blob)
    blob = blob_client.get_blob_properties()
    downloader = blob_client.download_blob()  # type: azure.storage.blob.StorageStreamDownloader

    # Send download file
    data = io.BytesIO(downloader.readall())
    data.seek(0)
    return flask.send_file(data, download_name=blob['name'],
                           mimetype=blob['content_settings']['content_type'])
