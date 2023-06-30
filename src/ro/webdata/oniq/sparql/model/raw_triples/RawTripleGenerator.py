from typing import List, Union

from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.nlp_utils import token_to_span, text_to_span
from ro.webdata.oniq.common.nlp.utils import WordnetUtils
from ro.webdata.oniq.common.nlp.word_utils import is_preposition, is_wh_word, is_aux
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.sparql.common.TokenHandler import TokenHandler
from ro.webdata.oniq.sparql.model.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class STATEMENT_TYPE:
    ADJECTIVE = "adjective"
    NOUN = "noun"
    PASS_POSS = "passive_possessive"


class RawTripleGenerator:
    def __init__(self, nl_question: NLQuestion):
        self.question = nl_question.question
        self.raw_triples = []

    def append_triple(self, token: Token, adjective: Token, triple_type: str):
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


class RDFTypeRawTriple:
    @staticmethod
    def generate_rdf_types(question: Span, triples: List[RawTriple]):
        rdf_types = []

        for statement in triples:
            RDFTypeRawTriple._append_rdf_type(question, rdf_types, statement.s)
            RDFTypeRawTriple._append_rdf_type(question, rdf_types, statement.o)

        return list(set(rdf_types))

    @staticmethod
    def _append_rdf_type(question: Span, rdf_types: List[RawTriple], entity: Union[str, AdjectiveEntity, NounEntity, Token]):
        rdf_type = RawTripleHandler.rdf_type_handler(question, entity)

        if rdf_type is not None:
            rdf_types.append(rdf_type)


class RawTripleHandler:
    @staticmethod
    def adj_before_noun_handler(sentence: Span, noun: Token, adjective: Token):
        country = WordnetUtils.find_country_by_nationality(adjective.text)

        if TokenHandler.adj_not_found(noun, adjective):
            # E.g.: "Give me all Swedish holidays." => Swedish -> Sweden
            # E.g.: "How high is the Yokohama Marine Tower?"
            return RawTriple(
                s=noun,
                p="country" if country is not None else token_to_span(adjective),
                o=NounEntity(adjective) if country is not None else AdjectiveEntity(adjective),
                question=sentence
            )

        return None

    @staticmethod
    def prep_after_noun_handler(sentence: Span, noun: Token):
        noun_entity = NounEntity(noun)

        if noun_entity.is_text():
            # E.g.: "When did the Ming dynasty dissolve?"
            return None

        rights = list(noun_entity.token.rights)
        prep = _get_prep(rights)

        if prep is not None:
            noun = TokenHandler.get_noun_after_prep(rights)

            if prep.lower_ == "in":
                if noun.ent_type_ == "GPE":
                    # E.g.: "What is the highest mountain in Romania?"
                    # E.g.: "Which museum in New York has the most visitors?"
                    return RawTriple(
                        s=NounEntity(noun_entity.token),
                        p=text_to_span("location"),
                        o=NounEntity(noun),
                        question=sentence
                    )
            elif prep.lower_ == "of":
                # E.g.: "Give me the currency of China."
                return RawTriple(
                    s=NounEntity(noun),
                    p=noun_entity.to_span(),
                    o=NounEntity(noun_entity.token),
                    question=sentence
                )

        return None

    @staticmethod
    def passive_possessive_handler(sentence: Span, token: Token):
        lefts = [token for token in list(token.lefts) if not is_wh_word(token)]
        rights = [token for token in list(token.rights) if not is_wh_word(token)]

        if len(rights) > 0 and is_aux(rights[0]):
            # E.g.: "Who is the person whose successor was Le Hong Phong?"  # possessive
            # E.g.: "Where was the person born whose successor was Le Hong Phong?"  # passive
            token = rights[0]
            noun_lefts = TokenHandler.get_nouns(list(token.lefts))
            noun_rights = TokenHandler.get_nouns(list(token.rights))

            if len(noun_lefts) > 0 and len(noun_rights) > 0:
                return RawTriple(
                    s=NounEntity(noun_lefts[0]),
                    p=token_to_span(noun_lefts[0]),
                    o=NounEntity(noun_rights[0]),
                    question=sentence
                )

        return None
    
    @staticmethod
    def rdf_type_handler(question: Span, entity: Union[str, AdjectiveEntity, NounEntity, Token]):
        text = entity if isinstance(entity, str) else entity.text
        entity_type = LookupService.local_resource_lookup(text)
    
        if entity_type is None:
            return None
    
        return RawTriple(
            s=entity,
            p="rdf:type",
            o=NounEntity(entity_type, entity.token, True),
            question=question
        )


def _get_prep(tokens: List[Token]):
    prep_rights = [prep for prep in tokens if is_preposition(prep)]

    if len(prep_rights) > 0:
        return prep_rights[0]

    return None
