from typing import List

from ro.webdata.oniq.sparql.model.final_triples.Triple import Triple
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class Triples:
    elements: List[Triple]

    def __init__(self, raw_triples: List[RawTriple]):
        self.elements = _init_triples(raw_triples)

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, item):
        return self.elements[item]

    def __str__(self):
        output = "[\n"
        for elem in self.elements:
            output += f"\t<{elem}>\n"
        output += "]"

        return output

    def append(self, triple: Triple):
        self.elements.append(triple)

    # # TODO: check
    # def unique(self):
    #     self.elements = list(set(self.elements))
    #
    # # TODO: check
    # def sort(self):
    #     self.elements = sorted(self.elements, key=lambda item: item.uri)
    #
    # # TODO: check
    # def exists(self, triple: Triple):
    #     return str(triple) in [str(elem) for elem in self.elements]
    #
    # # TODO: check
    # def find(self, triple: Triple):
    #     if self.exists(triple):
    #         filtered_props = [
    #             elem for elem in self.elements
    #             if str(elem) == str(triple)
    #         ]
    #
    #         return filtered_props[0]
    #
    #     return None


def _init_triples(raw_triples: List[RawTriple]):
    triples = []

    for raw_triple in raw_triples:
        triple = Triple(raw_triple)
        triples.append(triple)

    return triples
