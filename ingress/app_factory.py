import flask


def create_app() -> flask.Flask:
    app = flask.Flask(__name__)

    return app
