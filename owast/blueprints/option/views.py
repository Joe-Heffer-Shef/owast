import flask

app = flask.current_app
blueprint = flask.Blueprint('option', __name__, url_prefix='/option',
                            template_folder='templates')


@blueprint.route('/create', methods={'get', 'post'})
def create():
    return flask.render_template('option/create.html')


@blueprint.route('/<string:option_id>')
def detail(option_id):
    option = app.db.options.find_one_or_404(dict(_id=option_id))
    return flask.render_template('option/detail.html', option=option)


@blueprint.route('/')
def list_():
    options = app.mongo.db.options.find()
    return flask.render_template('option/list.html', options=options)


@blueprint.route('/<string:option_id>/delete/')
def delete():
    return flask.redirect(flask.url_for('option.list_'))
