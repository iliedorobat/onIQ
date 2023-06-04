import json
from typing import Union

import requests
from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.nlp_utils import text_to_span
from ro.webdata.oniq.common.text_utils import WORD_SEPARATOR
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.endpoint.models.RDFElement import RDFClass, RDFProperty
from ro.webdata.oniq.service.query_const import PATHS, ACCESSORS, VALUES
from ro.webdata.oniq.sparql.constants import SPARQL_STR_SEPARATOR
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.final_triples.predicate_utils import subject_predicate_lookup, object_predicate_lookup
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class Triple:
    def __init__(self, raw_triple: RawTriple):
        self.s = raw_triple.s
        self.p = _predicate_lookup(raw_triple)
        self.o = raw_triple.o
        self.question = raw_triple.question

        self.aggr = None
        self.order = None

    def __eq__(self, other):
        # only equality tests to other 'Triple' instances are supported
        if not isinstance(other, Triple):
            return NotImplemented
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        if self.p is None:
            return None

        if isinstance(self.p, PropertyMatcher):
            p = str(self.p.property)
        else:
            p = self.p

        s = self.s.to_var()
        o = self.o.to_var()

        return f"{s}   {p}   {o}"


def _predicate_lookup(raw_triple: RawTriple):
    subject: NounEntity = raw_triple.s
    predicate: Union[str, Span] = raw_triple.p
    obj: NounEntity = raw_triple.o
    question: Span = raw_triple.question

    if subject.is_res():
        if obj.is_var():
            return subject_predicate_lookup(question, subject, predicate)

    if subject.is_var():
        if obj.is_res():
            return object_predicate_lookup(question, obj, predicate)

    # E.g.: "Who is the tallest basketball player?"
    #       <?person   rdf:type   dbo:BasketballPlayer>
    return predicate


# def _node_lookup(noun_entity: NounEntity):
#     subject = noun_entity.to_var()

#     if subject.startswith("dbr:"):
#         target = noun_entity.compound_noun

#         if noun_entity.is_named_entity:
#             result = LookupService.entities_lookup(target)
#             return RDFClass(
#                 pydash.get(result, ["0", "resource", "0"], None),
#                 pydash.get(result, ["0", "type"], []),
#                 pydash.get(result, ["0", "label", "0"], None)
#             )
#         else:
#             resource_name = target.text.title().replace(WORD_SEPARATOR, SPARQL_STR_SEPARATOR)
#             # E.g.: "Where is Fort Knox located?"
#             resource = LookupService.resource_lookup(resource_name)

#             if resource is None:
#                 result = LookupService.noun_chunk_lookup(target)
#                 resource = RDFClass(
#                     pydash.get(result, ["0", "resource", "0"], None),
#                     pydash.get(result, ["0", "type"], []),
#                     pydash.get(result, ["0", "label", "0"], None)
#                 )

#             return resource

#     return subject


# def _prepare_predicate(subject: Union[str, RDFClass], raw_predicate:  Union[str, Token]):
#     predicate = ""

#     if isinstance(subject, RDFClass) and isinstance(raw_predicate, Token):
#         resource = str(subject)
#         # TODO:
#         return LookupService.property_lookup("Queen_Victoria", raw_predicate, None)

#     return predicate
