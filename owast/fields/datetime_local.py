import datetime


def datetime_local_default(t: datetime.datetime = None) -> datetime.datetime:
    """
    Current timestamp with timezone floored to minute resolution (which is the
    resolution of HTML5 datetime-local e.g. "2018-06-14T00:00"

    https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/datetime-local
    """
    t = t or datetime.datetime.utcnow()
    return t.replace(microsecond=0)