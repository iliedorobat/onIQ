from typing import Union

from spacy.tokens import Token

from ro.webdata.oniq.common.nlp.nlp_utils import token_to_span
from ro.webdata.oniq.sparql.NLQuestion import NLQuestion
from ro.webdata.oniq.sparql.NounEntity import NounEntity
from ro.webdata.oniq.sparql.triples.raw_triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.triples.raw_triples.generator.RawTripleHandler import RawTripleHandler


class STATEMENT_TYPE:
    ADJECTIVE = "adjective"
    NOUN = "noun"
    PASS_POSS = "passive_possessive"


class RawTripleGenerator:
    def __init__(self, nl_question: NLQuestion):
        self.question = nl_question.question
        self.raw_triples = []

    def append_triple(self, token: Token, adjective: Union[None, Token], triple_type: str):
        statement = None

        if triple_type == STATEMENT_TYPE.ADJECTIVE:
            statement = RawTripleHandler.adj_before_noun_handler(self.question, token, adjective)
        elif triple_type == STATEMENT_TYPE.NOUN:
            statement = RawTripleHandler.prep_after_noun_handler(self.question, token)
        elif triple_type == STATEMENT_TYPE.PASS_POSS:
            statement = RawTripleHandler.passive_possessive_handler(self.question, token)

        if statement is not None:
            self.raw_triples.append(statement)

    def append_noun_triple(self, s: Token, p: Union[str, Token], o: Token):
        # E.g.: "Is Barack Obama a democrat?"
        # E.g.: "Who is the youngest Pulitzer Prize winner?"
        predicate = p if isinstance(p, str) else token_to_span(p)

        statement = RawTriple(
            s=NounEntity(s),
            p=predicate,
            o=NounEntity(o),
            question=self.question
        )

        if statement is not None:
            self.raw_triples.append(statement)
