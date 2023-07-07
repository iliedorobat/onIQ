from typing import List, Union

from spacy.tokens import Span, Token

from ro.webdata.oniq.sparql.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.NounEntity import NounEntity
from ro.webdata.oniq.sparql.triples.raw_triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.triples.raw_triples.generator.RawTripleHandler import RawTripleHandler


class RDFTypeRawTriple:
    @staticmethod
    def generate_rdf_types(question: Span, triples_values: List[RawTriple]):
        rdf_types = []

        for statement in triples_values:
            RDFTypeRawTriple._append_rdf_type(question, rdf_types, statement.s)
            RDFTypeRawTriple._append_rdf_type(question, rdf_types, statement.o)

        return rdf_types

    @staticmethod
    def _append_rdf_type(question: Span, rdf_types: List[RawTriple], entity: Union[str, AdjectiveEntity, NounEntity, Token]):
        span = entity.to_span()

        # TODO: complete the list of exceptions
        if isinstance(span, Span):
            # E.g.: "How large is the area of UK?"
            contains_area = "area" in span.text.lower()

            # E.g.: "What is the nick name of Baghdad?"
            contains_name = "name" in span.text.lower()

            # E.g.: "How much is the population of Mexico City ?"
            contains_population = "population" in span.text.lower()

            # E.g.: "how much is the total population of  european union?"
            contains_total = "total" in span.text.lower()

            if contains_area or contains_total or contains_population or contains_name:
                return None

        rdf_type = RawTripleHandler.rdf_type_handler(question, entity)

        if rdf_type is not None:
            if rdf_type not in rdf_types:
                rdf_types.append(rdf_type)
