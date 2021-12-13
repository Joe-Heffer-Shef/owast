import flask

blueprint = flask.Blueprint('main', __name__, template_folder='templates')

app = flask.current_app


@blueprint.route('/')
def home():
    return flask.render_template('main/home.html')


@blueprint.route('/search')
def search():
    collections = {schema['title']: schema['collection']
                   for schema in app.mongo.db.schemas.find()}

    return flask.render_template('main/search.html', collections=collections)
