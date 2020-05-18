# TODO: complete the map
NAMED_ENTITY_MAP = {
    # TODO: CARDINAL = Numerals that do not fall under another type
    'CARDINAL': ['number', 'value'],
    'DATE': ['date', 'day', 'month', 'period', 'time', 'year'],
    'EVENT': ['battle', 'event', 'hurricane', 'sport', 'war'],
    'FAC': ['airport', 'bridge', 'building', 'highway', 'road'],
    'GPE': ['city', 'county', 'country', 'locality', 'location', 'state', 'town', 'village'],
    'LANGUAGE': ['language'],
    # TODO: LOC = Non-GPE locations, mountain ranges, bodies of water
    'LOC': ['location'],
    'LAW': ['document'],
    'MONEY': ['unit', 'value'],
    'NORP': ['nationality', 'politic', 'religion'],
    # TODO:
    'ORDINAL': ['first', 'second', 'third'],
    'ORG': ['agency', 'company', 'corporation', 'institution'],
    'PERCENT': ['value'],
    'PERSON': ['man', 'person', 'woman'],
    # TODO: PRODUCT = Not services
    'PRODUCT': ['food', 'object', 'vehicle'],
    'QUANTITY': ['distance', 'measurement', 'quantity', 'weight'],
    # TODO: TIME = time smaller than a day
    'TIME': ['date', 'minute', 'second', 'time'],
    'WORK_OF_ART': ['art', 'book', 'song']
}
