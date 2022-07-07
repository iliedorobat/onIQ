# TODO: complete the types of questions
class QUESTION_TYPES:
    ASK = "ask"
    COUNT = "count"  # how many, how much, how often
    HOW = "how"
    WHAT = "what"
    WHEN = "when"
    WHERE = "where"
    WHICH = "which"
    WHO = "who"
    WHOM = "whom"
    WHOSE = "whose"
    WHY = "why"


class TEST_MODES:
    DEFAULT = None
    LOCAL_TEST = "local_test"
    GLOBAL_TEST = "global_test"


class GLOBAL_ENV:
    IS_DEBUG = True
    IS_DEBUG_EXTRA = False
    TEST_MODE = TEST_MODES.GLOBAL_TEST


class PRINT_MODE:
    PRINT_ACTION = False
    PRINT_STATEMENT = True
    PRINT_TARGET = True
    PRINT_TOKEN = True


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


# TODO: remove
class LOGICAL_OPERATIONS:
    AND = 'conjunction'
    OR = 'disjunction'


class LOGICAL_OPERATORS:
    AND = '&&'
    OR = '||'


class PREFIX:
    VARIABLE = '?'


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


class SENTENCE_TYPE:
    PRON = "Pronoun Sentence"
    WH = "WH Sentence"
    WH_PRON_START = "WH Pronoun Start Sentence"
    WH_START = "WH Start Sentence"
    SELECT_CLAUSE = "Select Clause"
    WHERE_CLAUSE = "Where clause"


class SEPARATOR:
    NAMESPACE = ":"  # deprecated in favour of NAMESPACE_SEPARATOR
    STRING = "_"
    TRIPLE_PATTERN = " "


class SYSTEM_MESSAGES:
    METHOD_IS_OBSOLETE = "The method is obsolete and should be updated!"
    METHOD_NOT_TESTED = "The method has not been tested!"
    METHOD_NOT_USED = "The method is not used anymore!"
    METHOD_USED_WITH_SPACY_2 = "The method is intended to be used with Spacy v2"


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
