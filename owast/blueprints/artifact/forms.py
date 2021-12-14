import flask_wtf
from wtforms import DateTimeLocalField, FileField
from wtforms.validators import InputRequired

from owast.fields.objectid_input import ObjectIdStringField
from owast.fields.json_textarea import JsonTextAreaField
import owast.fields.datetime_local


class ArtifactForm(flask_wtf.FlaskForm):
    """
    A form to create or modify an artifact
    """

    class Meta:
        # Use flask-seasurf instead of wtforms CSRF protection
        csrf = False

    experiment_id = ObjectIdStringField(render_kw=dict(readonly=True))
    time = DateTimeLocalField(
        default=owast.fields.datetime_local.datetime_local_default,
        description='When the entity started to be used',
        format='%Y-%m-%dT%H:%M'
    )
    file = FileField(validators=[InputRequired()])
    attributes = JsonTextAreaField(render_kw={'class': 'text-monospace'})
