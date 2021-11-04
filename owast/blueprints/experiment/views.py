import flask
import pymongo

blueprint = flask.Blueprint('experiment', __name__, url_prefix='/experiment', template_folder='templates')


def get_db():
    client = pymongo.MongoClient('meta')
    db = client.owast

    return db


@blueprint.route('/')
def list_():
    db = get_db()
    return flask.render_template('experiment/list.html', experiments=db.experiment.find())


@blueprint.route('/create')
def create():
    """
    Write new experiment metadata and file upload.
    """

    if flask.request.method == 'POST':
        # TODO add experiment to database
        pass

    return flask.render_template('experiment/create.html')


@blueprint.route('/<string:experiment_id>')
def detail(experiment_id: str):
    db = get_db()

    db.experiment.find_one(dict(experiment_id=experiment_id))

    # TODO create SAS token for Azure Blob Storage
    # this will be passed to Javascript for temporary authentication

    # TODO File upload
    # https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-nodejs

    # Uploading Large Files in Windows Azure Blob Storage Using Shared Access Signature, HTML, and JavaScript
    # https://docs.microsoft.com/en-us/answers/questions/535512/how-to-upload-large-files-in-chunks-in-azure-blobs.html

    return flask.render_template('experiment/detail.html')
