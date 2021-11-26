import flask

app = flask.current_app
blueprint = flask.Blueprint('tool', __name__, url_prefix='/tool',
                            template_folder='templates')


@blueprint.route('/create')
def create():
    option_names = {'Supplier'}
    options = app.mongo.db.options.find(dict(name={'$in': list(option_names)}))
    return flask.render_template('tool/create.html', options=options)


# TODO use ObjectId converter
@blueprint.route('/<string:tool_id>')
def detail(tool_id):
    tool = app.db.tools.find_one_or_404(dict(_id=tool_id))
    return flask.render_template('tool/detail.html', tool=tool)


@blueprint.route('/')
def list_():
    tools = app.mongo.db.tools.find()
    return flask.render_template('tool/list.html', tools=tools)


@blueprint.route('/<string:tool_id>/delete/')
def delete():
    return flask.redirect(flask.url_for('tool.list_'))
