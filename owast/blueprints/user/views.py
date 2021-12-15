import flask
import flask_login

from .models import User

app = flask.current_app
blueprint = flask.Blueprint('user', __name__, url_prefix='/user',
                            template_folder='templates')


@blueprint.route('/test')
def test():
    return 'Hello world!'


@blueprint.route('/detail')
def detail():
    user = flask_login.current_user
    return flask.render_template('user/detail.html')


@blueprint.route('/login')
def login():
    return User.get_auth_flow()


@blueprint.route('/config')
def config():
    return flask.jsonify(User.get_config())
