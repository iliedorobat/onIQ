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


SENTENCE_TYPE = {
    "SELECT_CLAUSE": "select clause",
    "WHERE_CLAUSE": "where clause",

    "PRONOUN": "pronoun sentence",
    "WH_PRONOUN_START": "WH Pronoun start sentence",
    "WH_START": "WH start sentence"
}
