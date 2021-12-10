import itertools

# Influence map
# https://www.w3.org/TR/prov-dm/#concept-influence
# Which relations should be used to connect each type?
# https://www.w3.org/TR/prov-dm/#prov-dm-types-and-relations
# Mapping[FromType[ToType][Relation]]
PROV_RELATION = dict(
    Activity=dict(
        Activity='wasInformedBy',
        Entity='used',
        Agent='wasAssociatedWith',
    ),
    Entity=dict(
        Activity='wasGeneratedBy',
        Entity='wasDerivedFrom',
        Agent='wasAttributedTo',
    ),
    Agent=dict(
        # https://www.w3.org/TR/prov-dm/#concept-delegation
        Agent='actedOnBehalfOf',
    ),
)  # type: Mapping[str, Mapping[str, str]]

# Generic relation between any two types
DEFAULT_RELATION = 'wasInfluencedBy'

# Flatten the mapping to a linear list of all the relation types
RELATION_TYPES = set(itertools.chain((s for d in PROV_RELATION.values() for s
                                      in d.values()), (DEFAULT_RELATION,)))
