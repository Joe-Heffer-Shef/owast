import json

import flask_wtf
import wtforms
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import Length


def json_string(_, field: wtforms.Field):
    json.loads(field.data)


class ObjectIdStringField(HiddenField):
    """
    String field for BSON object identifier.

    https://docs.mongodb.com/manual/reference/method/ObjectId/
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators = list(self.validators) + [Length(min=24, max=24)]


class WasInfluencedByForm(flask_wtf.FlaskForm):
    """
    Relation properties for the default (base class)

    PROV-N notation:
    wasInfluencedBy(id; o2, o1, attrs)

    influencer (o1) <- wasInfluencedBy <- influencee (o2)

    https://www.w3.org/TR/prov-dm/#concept-influence
    """

    class Meta:
        # Use flask-seasurf instead of wtforms CSRF protection
        csrf = False

    influencee_schema_id = ObjectIdStringField()
    influencee_id = ObjectIdStringField()  # o2
    influencer_schema_id = ObjectIdStringField()
    influencer_id = ObjectIdStringField()  # o1
    attributes = TextAreaField(  # attrs
        validators=[json_string],
        default='{}',
        render_kw={'class': 'text-monospace form-control'},
    )
