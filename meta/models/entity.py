import pymodm


class Entity(pymodm.MongoModel):
    """
    prov:Entity
    https://www.w3.org/TR/prov-dm/#term-entity

    An entity is a physical, digital, conceptual, or other kind of thing with
    some fixed aspects; entities may be real or imaginary.
    """
    # an identifier for an object
    id = pymodm.CharField(primary_key=True)

    # an optional set of attribute-value pairs representing additional
    # information about this activity
    # e.g. {prov:location="Le Louvre, Paris", prov:type="StillImage"}
    attributes = pymodm.DictField()
