from typing import Union

import pydash
from spacy.tokens import Span, Token

from ro.webdata.oniq.common.text_utils import WORD_SEPARATOR
from ro.webdata.oniq.endpoint.common.match.PropertiesMatcher import PropertiesMatcher
from ro.webdata.oniq.endpoint.common.translator.CSVTranslator import CSVTranslator
from ro.webdata.oniq.endpoint.dbpedia.constants import DBPEDIA_CLASS_TYPES
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.endpoint.models.RDFElement import RDFClass
from ro.webdata.oniq.sparql.constants import SPARQL_STR_SEPARATOR
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


props = CSVTranslator.to_props()


class Triple:
    def __init__(self, raw_triple: RawTriple):
        self.s = raw_triple.s
        self.p = _prepare_predicate(raw_triple.p)
        self.o = raw_triple.o

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

        s = self.s.to_var()
        p = str(self.p.property)
        o = self.o.to_var()

        return f"{s}   {p}   {o}"


def _prepare_predicate(predicate: Union[str, Span]):
    if isinstance(predicate, Span):
        # TODO: result_type=DBPEDIA_CLASS_TYPES.PLACE
        return PropertiesMatcher.get_best_matched(props, predicate, None)
    return None


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
