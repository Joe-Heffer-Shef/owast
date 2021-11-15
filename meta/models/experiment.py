import pymodm

import meta.models.prov


class Experiment(pymodm.MongoModel, meta.models.prov.Activity):
    name = pymodm.CharField(primary_key=True)
