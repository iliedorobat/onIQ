import json
from typing import Union

import requests
from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.nlp_utils import text_to_span
from ro.webdata.oniq.common.text_utils import WORD_SEPARATOR
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.endpoint.models.RDFElement import RDFClass, RDFProperty
from ro.webdata.oniq.service.query_const import PATHS, ACCESSORS, VALUES
from ro.webdata.oniq.sparql.constants import SPARQL_STR_SEPARATOR
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class Triple:
    def __init__(self, raw_triple: RawTriple):
        self.s = raw_triple.s
        self.p = _prepare_predicate(raw_triple.p, raw_triple.question)
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


def _prepare_predicate(predicate: Union[str, Span], question: Span):
    if isinstance(predicate, Span):
        matcher_uri = f'http://localhost:8200/{PATHS.MATCHER}?' \
                      f'{ACCESSORS.QUESTION}={question}&' \
                      f'{ACCESSORS.START_I}={predicate.start}&' \
                      f'{ACCESSORS.END_I}={predicate.end}&' \
                      f'{ACCESSORS.TARGET_TYPE}={VALUES.SPAN}'

        return _prepare_span_predicate(predicate, matcher_uri)

    elif isinstance(predicate, str):
        if predicate not in ["rdf:type"]:
            matcher_uri = f'http://localhost:8200/{PATHS.MATCHER}?' \
                          f'{ACCESSORS.QUESTION}={question}&' \
                          f'{ACCESSORS.TARGET_EXPRESSION}={predicate}&' \
                          f'{ACCESSORS.TARGET_TYPE}={VALUES.STRING}'

            return _prepare_span_predicate(text_to_span(predicate), matcher_uri)

    return predicate


def _prepare_span_predicate(predicate: [str, Span], matcher_uri: str):
    matcher_response = requests.get(matcher_uri)
    matcher_json = json.loads(matcher_response.content)
    prop_matcher = json.loads(matcher_json['property'])
    prop = RDFProperty(
        prop_matcher["uri"],
        prop_matcher["parent_uris"],
        prop_matcher["label"],
        prop_matcher["ns"],
        prop_matcher["ns_label"],
        prop_matcher["res_domain"],
        prop_matcher["res_range"]
    )
    best_matched = PropertyMatcher(prop, predicate, None)

    return best_matched


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
