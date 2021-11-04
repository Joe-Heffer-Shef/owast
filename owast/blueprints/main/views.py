import flask

blueprint = flask.Blueprint('main', __name__, template_folder='templates')


@blueprint.route('/')
def home():
    return flask.render_template('main/home.html')
