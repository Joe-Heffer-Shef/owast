import pymodm


class Activity(pymodm.MongoModel):
    """
    prov:Activity
    https://www.w3.org/TR/prov-dm/#term-Activity

    An activity is something that occurs over a period of time and acts upon
    or with entities; it may include consuming, processing, transforming,
    modifying, relocating, using, or generating entities.
    """

    # an identifier for an object
    id = pymodm.CharField(primary_key=True)

    # an optional set of attribute-value pairs representing additional
    # information about this activity
    # e.g. {prov:location="Le Louvre, Paris", prov:type="StillImage"}
    attributes = pymodm.DictField()

    # time for the start of the activity
    start_time = pymodm.DateTimeField(required=False)

    # time for the end of the activity
    end_time = pymodm.DateTimeField(required=False)
