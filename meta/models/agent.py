import pymodm


class Agent(pymodm.MongoModel):
    """
    prov:Agent
    https://www.w3.org/TR/prov-dm/#concept-agent

    An agent is something that bears some form of responsibility for an
    activity taking place, for the existence of an entity, or for another
    agent's activity.
    """

    # an identifier for an object
    id = pymodm.CharField(primary_key=True)

    # an optional set of attribute-value pairs representing additional
    # information about this activity
    # e.g. {prov:location="Le Louvre, Paris", prov:type="StillImage"}
    attributes = pymodm.DictField()
