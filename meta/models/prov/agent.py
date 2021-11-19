import pymodm

import meta.models.prov


class Agent(pymodm.MongoModel, meta.models.ProvMixin):
    """
    PROV-DM Type prov:Agent
    https://www.w3.org/TR/prov-dm/#concept-agent

    An agent is something that bears some form of responsibility for an
    activity taking place, for the existence of an entity, or for another
    agent's activity.
    """

    # an optional set of attribute-value pairs representing additional
    # information about this activity
    # e.g. {prov:location="Le Louvre, Paris", prov:type="StillImage"}
    attributes = pymodm.DictField()
