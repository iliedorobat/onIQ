from typing import List

from ro.webdata.oniq.sparql.filters.Filter import Filter, FILTER_FUNCTION, COMPARISON_OPERATORS
from ro.webdata.oniq.sparql.filters.YearsHandler import YearTracker
from ro.webdata.oniq.sparql.triples.Triple import Triple


AFTER_INDICATORS = [
    "after",
    "beyond",
    "later than",
    "posterior to",
]

SINCE_INDICATORS = [
    "from",
    "since"
]

BEFORE_INDICATORS = [
    "anterior to",
    "before",
    "behind",
    "earlier than",
    "previous to",
    "prior to",
    "until",
    "up to"
]


class Filters:
    def __init__(self, triples_values: List[Triple]):
        self.values = init_filters(triples_values)


def init_filters(triples_values: List[Triple]):
    filters = []

    for triple in triples_values:
        year = YearTracker(triple.s.token)
        if year.exists():
            operator = _get_operator(year.ante_notation)
            filters.append(
                Filter(triple.s, year.value, operator, FILTER_FUNCTION.YEAR)
            )

        year = YearTracker(triple.o.token)
        if year.exists():
            operator = _get_operator(year.ante_notation)
            filters.append(
                Filter(triple.o, year.value, operator, FILTER_FUNCTION.YEAR)
            )

    return filters


def _get_operator(ante_notation: str):
    if ante_notation in SINCE_INDICATORS:
        return COMPARISON_OPERATORS.GTE
    elif ante_notation in AFTER_INDICATORS:
        return COMPARISON_OPERATORS.GT
    elif ante_notation in BEFORE_INDICATORS:
        return COMPARISON_OPERATORS.LT
    return COMPARISON_OPERATORS.EQ
