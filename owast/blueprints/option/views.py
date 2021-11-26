import flask
import pymongo.collection
import pymongo.results
import flask_pymongo.wrappers
from bson.objectid import ObjectId

app = flask.current_app
blueprint = flask.Blueprint('option', __name__, url_prefix='/option',
                            template_folder='templates')


@blueprint.route('/create', methods={'GET', 'POST'})
def create():
    """
    Create a new option with multiple values.
    """
    if flask.request.method == 'POST':
        # Create new document
        options = app.mongo.db.options  # type: pymongo.collection.Collection
        option = dict(
            name=flask.request.form['name'],
            values=[value for key, value in flask.request.form.items() if
                    key.startswith('value')]
        )
        result = options.insert_one(
            option)  # type: pymongo.results.InsertOneResult
        app.logger.info(result)
        flask.flash(f"Created {option['name']}")

        return flask.redirect(
            flask.url_for('option.detail', option_id=result.inserted_id))

    return flask.render_template('option/create.html')


@blueprint.route('/<ObjectId:option_id>')
def detail(option_id: ObjectId):
    """
    Show a single option with its set of values.
    """
    options = app.mongo.db.options  # type: flask_pymongo.wrappers.Collection
    option = options.find_one_or_404(option_id)
    return flask.render_template('option/detail.html', option=option)


@blueprint.route('/')
def list_():
    options = app.mongo.db.options.find()
    return flask.render_template('option/list.html', options=options)


@blueprint.route('/<ObjectId:option_id>/delete')
def delete(option_id: ObjectId):
    options = app.mongo.db.options  # type: flask_pymongo.wrappers.Collection
    result = options.delete_one(
        dict(_id=option_id))  # type: pymongo.results.DeleteResult
    app.logger.info(result.raw_result)
    flask.flash(f'Deleted {option_id}')
    return flask.redirect(flask.url_for('option.list_'))


@blueprint.route('/<ObjectId:option_id>/edit')
def edit(option_id: ObjectId):
    """
    Edit the values of this option
    """
    options = app.mongo.db.options  # type: flask_pymongo.wrappers.Collection
    option = options.find_one_or_404(option_id)
    return flask.render_template('option/edit.html', option=option)
