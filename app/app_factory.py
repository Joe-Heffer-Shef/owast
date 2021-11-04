import flask


def create_app() -> flask.Flask:
    app = flask.Flask('owast')

    # TODO LDAP authentication (Active Directory)

    return app
