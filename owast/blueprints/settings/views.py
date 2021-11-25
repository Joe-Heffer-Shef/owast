import flask

app = flask.current_app
blueprint = flask.Blueprint('settings', __name__, url_prefix='/settings',
                            template_folder='templates')


@blueprint.route('/')
def settings():
    return flask.render_template('settings/settings.html')
