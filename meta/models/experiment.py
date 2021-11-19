import pymodm

import meta.models.prov


class Experiment(pymodm.MongoModel, meta.models.prov.Activity):
    """
    An experiment activity.
    """
    pass
