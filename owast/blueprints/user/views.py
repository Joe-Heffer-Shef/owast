import flask
import flask_login
import requests

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
    return flask.render_template('user/detail.html', user=user)


@blueprint.route('/login')
def login():
    auth_flow = User.get_auth_flow()
    for key, value in auth_flow.items():
        app.logger.debug(f"{key}: {value}")
    # return flask.redirect(auth_flow['auth_uri'])
    response = requests.get(auth_flow['auth_uri'])
    response.raise_for_status()
    return response.content


@blueprint.route('/config')
def config():
    return flask.jsonify(User.get_config())
