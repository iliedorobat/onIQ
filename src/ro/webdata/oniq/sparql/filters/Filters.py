from typing import List

from ro.webdata.oniq.sparql.model.final_triples.Triple import Triple


class Filters:
    def __init__(self, triples: List[Triple]):
        self.values = init_filters(triples)


def init_filters(triples: List[Triple]):
    return []
