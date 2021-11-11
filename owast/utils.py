import datetime

import flask


def get_metadata() -> dict:
    """
    Load multiple metadata fields from a form submission
    """

    meta = dict()

    # Iterate over any number of custom metadata fields
    i = 1
    while True:
        try:
            key = flask.request.form[f'meta_{i}_key']
        except KeyError:
            break
        value = flask.request.form[f'meta_{i}_value']

        meta[key] = value

        i += 1

    return meta


def html_datetime(time: datetime.datetime = None) -> str:
    """
    Generate a timestamp for use in HTML forms.

    https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/datetime-local
    """
    # Default to current timestamp
    time = time or datetime.datetime.utcnow()
    # Reduce the resolution
    time = time.replace(microsecond=0)
    # Standard timestamp
    return time.isoformat()
