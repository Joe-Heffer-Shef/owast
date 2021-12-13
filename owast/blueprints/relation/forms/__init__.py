import flask_wtf
from wtforms import SelectField
from wtforms.validators import DataRequired

from owast.fields.json_textarea import JsonTextAreaField
from owast.fields.objectid_input import ObjectIdStringField
from ..constants import DEFAULT_RELATION, RELATION_TYPES


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

    type = SelectField(default=DEFAULT_RELATION, validators=[DataRequired()],
                       choices=RELATION_TYPES, render_kw=dict(readonly=True))
    influencee_schema_id = ObjectIdStringField(validators=[DataRequired()])
    influencee_id = ObjectIdStringField(validators=[DataRequired()])  # o2
    influencer_schema_id = ObjectIdStringField(validators=[DataRequired()])
    influencer_id = ObjectIdStringField(validators=[DataRequired()])  # o1
    attributes = JsonTextAreaField(  # attrs
        default='{}',
        description="JSON object (key-value pairs)",
        render_kw={'class': 'text-monospace form-control'},
    )
