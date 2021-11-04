import flask


def create_app() -> flask.Flask:
    app = flask.Flask(__name__)

    # TODO LDAP authentication (Active Directory)

    return app
