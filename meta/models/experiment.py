import pymodm

import meta.models.prov


class Experiment(pymodm.MongoModel, meta.models.prov.ProvMixin):
    """
    Experiment
    """

    # an optional set of attribute-value pairs representing additional
    # information about this activity
    # e.g. {prov:location="Le Louvre, Paris", prov:type="StillImage"}
    attributes = pymodm.DictField()

    # time for the start of the activity
    start_time = pymodm.DateTimeField(required=False)

    # time for the end of the activity
    end_time = pymodm.DateTimeField(required=False)
