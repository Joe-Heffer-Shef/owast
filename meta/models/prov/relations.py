import pymodm

from meta.models.prov.entity import Entity
from meta.models.prov.activity import Activity


class WasGeneratedBy(pymodm.MongoModel):
    """
    Generation is the completion of production of a new entity by an activity.
    This entity did not exist before generation and becomes available for usage
    after this generation.

    https://www.w3.org/TR/2013/REC-prov-dm-20130430/#dfn-wasgeneratedby
    """

    entity = pymodm.ReferenceField(Entity, required=True)
    activity = pymodm.ReferenceField(Activity, required=True)
    time = pymodm.DateTimeField()
    attributes = pymodm.DictField()
