import flask
import pymongo.collection
import pymongo.results
from bson.objectid import ObjectId

app = flask.current_app
blueprint = flask.Blueprint('tool', __name__, url_prefix='/tool',
                            template_folder='templates')


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    if flask.request.method == 'POST':
        tool = {key: value for key, value in flask.request.form.items() if
                not key.startswith('_')}
        tools = app.mongo.db.tools  # type: pymongo.collection.Collection
        result = tools.insert_one(
            tool)  # type: pymongo.results.InsertOneResult
        app.logger.info(result)
        flask.flash(f"Created {result.inserted_id}")

    option_names = {'Supplier'}
    options = app.mongo.db.options.find(dict(name={'$in': list(option_names)}))
    return flask.render_template('tool/create.html', options=options)


# TODO use ObjectId converter
@blueprint.route('/<ObjectId:tool_id>')
def detail(tool_id: ObjectId):
    tool = app.mongo.db.tools.find_one_or_404(tool_id)
    return flask.render_template('tool/detail.html', tool=tool)


@blueprint.route('/')
def list_():
    tools = app.mongo.db.tools.find()
    return flask.render_template('tool/list.html', tools=tools)


@blueprint.route('/<string:tool_id>/delete/')
def delete():
    return flask.redirect(flask.url_for('tool.list_'))
