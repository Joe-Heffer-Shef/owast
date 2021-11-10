import flask

import owast.blob

app = flask.current_app
blueprint = flask.Blueprint('blob', __name__, url_prefix='/blob',
                            template_folder='templates')
service_client = owast.blob.get_service_client()


@blueprint.route('/')
def list_():
    blobs = service_client.list_blobs()

    return flask.render_template('blob/list.html', blobs=blobs)


@blueprint.route('/<string:container>/<string:blob>')
def detail(container: str, blob: str):
    blob_client = service_client.get_blob_client(
        container=container, blob=blob)

    blob = blob_client.get_blob_properties()

    return flask.render_template('blob/detail.html', blob=blob)


@blueprint.route('/<string:container>/<string:blob>/delete')
def delete(container: str, blob: str):
    blob_client = service_client.get_blob_client(
        container=container, blob=blob)

    blob_client.delete_blob()

    flask.flash(f'Deleted blob "{container}/{blob}"')

    return flask.redirect(
        flask.url_for('container.detail', container=container))
