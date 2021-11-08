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
