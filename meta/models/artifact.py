import pymodm

import meta.models.prov


class Artifact(pymodm.MongoModel, meta.models.prov.Entity):
    pass
