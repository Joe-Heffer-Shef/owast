import flask
import owast.blob

app = flask.current_app
blueprint = flask.Blueprint('container', __name__, url_prefix='/container',
                            template_folder='templates')
service_client = owast.blob.get_service_client()


@blueprint.route('/')
def list_():
    containers = service_client.list_containers()

    return flask.render_template('container/list.html', containers=containers)


@blueprint.route('/<string:container_name>')
def detail(container_name: str):
    container_client = service_client.get_container_client(
        container=container_name)

    container = container_client.get_container_properties()

    blobs = container_client.list_blobs()

    return flask.render_template('container/detail.html',
                                 container=container, blobs=blobs)
