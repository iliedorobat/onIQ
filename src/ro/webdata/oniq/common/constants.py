class TEST_MODES:
    DEFAULT = None
    LOCAL_TEST = "local_test"
    GLOBAL_TEST = "global_test"


class GLOBAL_ENV:
    IS_DEBUG = True
    IS_DEBUG_EXTRA = False
    TEST_MODE = TEST_MODES.DEFAULT


class PRINT_MODE:
    PRINT_TOKEN = True
    PRINT_DEPS = True


class COMPARISON_OPERATORS:
    CONTAINS = 'contains'
    NOT_CONTAINS = '!contains'
    REGEX = 'regex'
    EQ = '='
    NOT_EQ = '!='
    GT = '>'
    GTE = '>='
    LT = '<'
    LTE = '<='


class LOGICAL_OPERATORS:
    AND = '&&'
    OR = '||'


PRONOUNS = [
    "i", "me",
    "you", "thee",
    "he", "him",
    "she", "her",
    "it",
    "we", "us",
    "they", "them",
    "its"
]


# TODO: complete the map
NAMED_ENTITY_MAP = {
    # TODO: CARDINAL = Numerals that do not fall under another type
    "CARDINAL": ["number", "value"],
    "DATE": ["date", "day", "month", "period", "time", "year"],
    "EVENT": ["battle", "event", "hurricane", "sport", "war"],
    "FAC": ["airport", "bridge", "building", "highway", "road"],
    "GPE": ["city", "county", "country", "locality", "location", "state", "town", "village"],
    "LANGUAGE": ["language"],
    # TODO: LOC = Non-GPE locations, mountain ranges, bodies of water
    "LOC": ["location"],
    "LAW": ["document"],
    "MONEY": ["unit", "value"],
    "NORP": ["nationality", "politic", "religion"],
    # TODO:
    "ORDINAL": ["first", "second", "third"],
    "ORG": ["agency", "company", "corporation", "institution"],
    "PERCENT": ["value"],
    "PERSON": ["man", "person", "woman"],
    # TODO: PRODUCT = Not services
    "PRODUCT": ["food", "object", "vehicle"],
    "QUANTITY": ["distance", "measurement", "quantity", "weight"],
    # TODO: TIME = time smaller than a day
    "TIME": ["date", "minute", "second", "time"],
    "WORK_OF_ART": ["art", "book", "song"]
}
