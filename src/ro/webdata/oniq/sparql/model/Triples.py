from typing import List, Union

from spacy.tokens import Token

from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.Triple import Triple


class Triples:
    elements: List[Triple]

    def __init__(self, elements: List[Triple]):
        self.elements = elements

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

    def append_triple(self, subject: Union[NounEntity, Token], predicate: Union[str, Token], obj: Union[str, Token, NounEntity]):
        triple = Triple(subject, predicate, obj)

        if not triple.is_valid():
            # E.g.: "Where is Fort Knox located?"
            return None

        self.elements.append(triple)
        return triple

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
