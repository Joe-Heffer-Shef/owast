from wtforms import DateTimeField
from . import WasInfluencedByForm


class UsedForm(WasInfluencedByForm):
    """
    Additional inputs for used relation

    https://www.w3.org/TR/prov-dm/#concept-usage
    """
    time = DateTimeField(render_kw=dict(type='datetime-local'))
