import flask

app = flask.current_app
blueprint = flask.Blueprint('user', __name__, url_prefix='/user',
                            template_folder='templates')
