import pymodm


class ResearchObject:
    """
    Base class
    """
    name = pymodm.fields.CharField()
    created = pymodm.fields.TimestampField()
    meta = pymodm.fields.DictField()
