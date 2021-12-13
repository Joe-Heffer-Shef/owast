from wtforms import DateTimeLocalField

from owast.fields.datetime_local import datetime_local_default
from . import WasInfluencedByForm


class UsedForm(WasInfluencedByForm):
    """
    Additional inputs for used relation

    https://www.w3.org/TR/prov-dm/#concept-usage
    """
    time = DateTimeLocalField(
        default=datetime_local_default,
        description='When the entity started to be used',
        format='%Y-%m-%dT%H:%M'
    )
