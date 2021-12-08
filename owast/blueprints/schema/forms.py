import flask_wtf
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired


class SchemaForm(flask_wtf.FlaskForm):
    """
    A form to create or modify a research object schema
    """

    class Meta:
        csrf = False

    title = StringField(validators=[InputRequired()])
    collection = StringField(description='The plural of the title')
    description = StringField()
    icon = StringField(
        description='See <a href="https://icons.getbootstrap.com/">Bootstrap Icons</a> list')
    properties = TextAreaField(default='{}', render_kw=dict(rows=8),
                               description='The schema properties defined using '
                                           '<a href="https://json-schema.org/">JSON Schema.</a>')
    required = TextAreaField(default='[]',
                             description='A JSON list of mandatory property names.')
