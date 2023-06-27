from typing import List, Union

from spacy.tokens import Span, Token

from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.sparql.model.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class RDFTypeTriple:
    @staticmethod
    def generate_rdf_types(question: Span, triples: List[RawTriple]):
        rdf_types = []

        for statement in triples:
            _append_rdf_type(question, rdf_types, statement.s)
            _append_rdf_type(question, rdf_types, statement.o)

        return list(set(rdf_types))


def _append_rdf_type(question: Span, rdf_types: List[RawTriple], entity: Union[str, AdjectiveEntity, NounEntity, Token]):
    rdf_type = _get_rdf_type(question, entity)

    if rdf_type is not None:
        rdf_types.append(rdf_type)


def _get_rdf_type(question: Span, entity: Union[str, AdjectiveEntity, NounEntity, Token]):
    text = entity if isinstance(entity, str) else entity.text
    # TODO: use DBpedia spotlight?
    entity_type = LookupService.local_resource_lookup(text)

    if entity_type is None:
        return None

    return RawTriple(
        s=entity,
        p="rdf:type",
        o=NounEntity(entity_type, entity.token, True),
        question=question
    )
