import flask_wtf
from wtforms import DateTimeLocalField, FileField
from wtforms.validators import InputRequired
from owast.fields.objectid_input import ObjectIdStringField
from owast.fields.json_textarea import JsonTextAreaField


class ArtifactForm(flask_wtf.FlaskForm):
    """
    A form to create or modify an artifact
    """

    class Meta:
        # Use flask-seasurf instead of wtforms CSRF protection
        csrf = False

    experiment_id = ObjectIdStringField()
    created_at = DateTimeLocalField()
    file = FileField(validators=[InputRequired()])
    attributes = JsonTextAreaField()
