import flask

blueprint = flask.Blueprint('experiment', __name__)


@blueprint.route('/create')
def create():
    return flask.render_template('experiment/create.html')
