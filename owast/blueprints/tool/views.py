import flask
import pymongo.collection
import pymongo.results
from bson.objectid import ObjectId
from .forms import ToolForm

app = flask.current_app
blueprint = flask.Blueprint('tool', __name__, url_prefix='/tool',
                            template_folder='templates')


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    form = ToolForm(flask.request.form)

    if form.validate_on_submit():
        # Create tool document
        tool = {key: value for key, value in form.data if key != 'csrf_token'}
        tools = app.mongo.db.tools  # type: pymongo.collection.Collection
        result = tools.insert_one(
            tool)  # type: pymongo.results.InsertOneResult
        app.logger.info(result)
        flask.flash(f"Created {result.inserted_id}")
        return flask.redirect(
            flask.url_for('tool.detail', tool_id=result.inserted_id))

    # Render form
    option_names = {'Supplier'}
    options = app.mongo.db.options.find(dict(name={'$in': list(option_names)}))
    return flask.render_template('tool/create.html', options=options,
                                 form=ToolForm())


@blueprint.route('/<ObjectId:tool_id>')
def detail(tool_id: ObjectId):
    tool = app.mongo.db.tools.find_one_or_404(tool_id)
    return flask.render_template('tool/detail.html', tool=tool)


@blueprint.route('/')
def list_():
    tools = app.mongo.db.tools.find()
    return flask.render_template('tool/list.html', tools=tools)


@blueprint.route('/<ObjectId:tool_id>/delete/')
def delete(object_id: ObjectId):
    result = app.mongo.db.tools.delete(
        dict(_id=object_id))  # type: pymongo.results.DeleteResult
    app.logger.info(result.raw_result)
    flask.flash(f"Deleted tool '{object_id}'")
    return flask.redirect(flask.url_for('tool.list_'))


@blueprint.route('/<ObjectId:tool_id>/edit')
def edit(tool_id: ObjectId):
    tool = app.mongo.db.tools.find_one_or_404(tool_id)
    form = ToolForm(flask.request.form, obj=tool)
    if form.validate_on_submit():
        raise NotImplementedError
    return flask.render_template('tool/edit.html', tool=tool, form=form)
