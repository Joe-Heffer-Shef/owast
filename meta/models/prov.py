import abc

import pymodm


class ProvObject(abc.ABC):
    """
    W3C PROV ontology abstract base class

    https://www.w3.org/TR/prov-o/
    https://www.w3.org/TR/prov-dm/
    """

    # an identifier for an object
    id = pymodm.CharField(primary_key=True)

    # an optional set of attribute-value pairs representing additional
    # information about this activity
    # e.g. {prov:location="Le Louvre, Paris", prov:type="StillImage"}
    attributes = pymodm.DictField()


class Activity(ProvObject):
    """
    prov:Activity
    https://www.w3.org/TR/prov-dm/#term-Activity

    An activity is something that occurs over a period of time and acts upon
    or with entities; it may include consuming, processing, transforming,
    modifying, relocating, using, or generating entities.
    """

    # time for the start of the activity
    start_time = pymodm.DateTimeField(required=False)

    # time for the end of the activity
    end_time = pymodm.DateTimeField(required=False)


class Entity(ProvObject):
    """
    prov:Entity
    https://www.w3.org/TR/prov-dm/#term-entity

    An entity is a physical, digital, conceptual, or other kind of thing with
    some fixed aspects; entities may be real or imaginary.
    """


class Agent(ProvObject):
    """
    prov:Agent
    https://www.w3.org/TR/prov-dm/#concept-agent

    An agent is something that bears some form of responsibility for an
    activity taking place, for the existence of an entity, or for another
    agent's activity.
    """
    pass


class SoftwareAgent(Agent):
    """
    A software agent is running software.
    """
    pass


class Person(Agent):
    """
    Person agents are people.
    """
    pass


class Organization(Agent):
    """
    An organization is a social or legal institution such as a company,
    society, etc.
    """
    pass
