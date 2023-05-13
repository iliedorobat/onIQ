from typing import List, Union

from spacy.tokens import Span, Token

from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.model.raw_triples.raw_target_utils import RawTargetUtils


class RawQuery:
    raw_triples: List[RawTriple]
    target_nouns: List[NounEntity]

    def __init__(self, sentence: Span):
        self.raw_triples = []
        self.sentence = sentence
        self.target_nouns = []

    def __len__(self):
        return len(self.raw_triples)

    def __getitem__(self, item):
        return self.raw_triples[item]

    def __str__(self, include_targets: bool = False):
        output = "target_nouns = [\n"
        for target_noun in self.target_nouns:
            output += f"\t{target_noun.to_var()}\n"
        output += "]\n"

        output += "raw_triples = [\n"
        for raw_triple in self.raw_triples:
            output += f"\t<{raw_triple}>\n"
        output += "]"

        return output

    def append_raw_triple(self, nl_question: NLQuestion, subject: Union[NounEntity, Token], predicate: Union[str, Span], obj: Union[str, Token, NounEntity]):
        raw_triple = RawTriple(subject, predicate, obj)

        if not raw_triple.is_valid():
            # E.g.: "Where is Fort Knox located?"
            return None

        self.raw_triples.append(raw_triple)
        RawTargetUtils.update_target_nouns(nl_question, self.target_nouns, self.sentence, raw_triple)
        return raw_triple

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
