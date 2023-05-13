from typing import List, Union

from spacy.tokens import Span
from spacy.tokens import Token

from ro.webdata.oniq.common.nlp.word_utils import is_noun
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


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

    def __str__(self):
        output = "[\n"
        for elem in self.raw_triples:
            output += f"\t<{elem}>\n"
        output += "]"

        return output

    def append_raw_triple(self, subject: Union[NounEntity, Token], predicate: Union[str, Span], obj: Union[str, Token, NounEntity]):
        raw_triple = RawTriple(subject, predicate, obj)

        if not raw_triple.is_valid():
            # E.g.: "Where is Fort Knox located?"
            return None

        self.raw_triples.append(raw_triple)
        _update_target_nouns(self.target_nouns, self.sentence, raw_triple)
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


def _update_target_nouns(target_nouns: List[NounEntity], sentence: Span, raw_triple: RawTriple):
    new_target_nouns = _get_target_nouns(sentence)
    
    for target_noun in new_target_nouns:
        if raw_triple.s.noun == target_noun:
            target_nouns.append(raw_triple.s)
        if raw_triple.o.noun == target_noun:
            target_nouns.append(raw_triple.o)


def _get_target_nouns(sentence: Span):
    target_nouns = []
    
    for token in sentence:
        if is_noun(token) and token.head == sentence.root:
            target_nouns.append(token)

    return target_nouns
