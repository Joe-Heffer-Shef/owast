import flask_wtf
from wtforms import StringField, TextAreaField, RadioField, BooleanField
from wtforms.validators import InputRequired

PROV_STRUCTURES = [
    'Entity',
    'Activity',
    'Agent',
]


class SchemaForm(flask_wtf.FlaskForm):
    """
    A form to create or modify a research object schema
    """

    class Meta:
        # Use flask-seasurf instead of wtforms CSRF protection
        csrf = False

    title = StringField(validators=[InputRequired()])
    collection = StringField(description='The plural of the title')
    description = StringField()
    prov_type = RadioField(
        label='PROV Type',
        choices=PROV_STRUCTURES,
        description='Which PROV data structure should be used to represent '
                    'this object.',
        validators=[InputRequired()],
    )
    icon = StringField(
        description='See <a href="https://icons.getbootstrap.com/">Bootstrap Icons</a> list')
    properties = TextAreaField(default='{}', render_kw=dict(rows=8),
                               description='The schema properties defined using '
                                           '<a href="https://json-schema.org/">JSON Schema.</a>')
    required = TextAreaField(default='[]',
                             description='A JSON list of mandatory property names.')
    starred = BooleanField(default=False)
