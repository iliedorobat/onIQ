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
        rdf_type = RawTripleHandler.rdf_type_handler(question, entity)

        if rdf_type is not None:
            if rdf_type not in rdf_types:
                rdf_types.append(rdf_type)
