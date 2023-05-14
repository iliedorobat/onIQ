from typing import Union

import pydash
from spacy.tokens import Token

from ro.webdata.oniq.common.text_utils import WORD_SEPARATOR
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.endpoint.models.RDFElement import RDFClass
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class Triple:
    def __init__(self, raw_triple: RawTriple):
        subject = _node_lookup(raw_triple.s)
        obj = _node_lookup(raw_triple.o)

        self.s = Node(subject)
        self.p = _prepare_predicate(subject, raw_triple.p)
        self.o = Node(obj)

        self.aggregation = None
        self.order = None

    def __eq__(self, other):
        # only equality tests to other 'Triple' instances are supported
        if not isinstance(other, Triple):
            return NotImplemented
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        s = str(self.s)
        p = str(self.p)
        o = str(self.o)

        return f"{s}   {p}   {o}"


class Node:
    def __init__(self, value: Union[str, RDFClass]):
        self.value = value

    def __eq__(self, other):
        # only equality tests to other 'Edge' instances are supported
        if not isinstance(other, Node):
            return NotImplemented
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return str(self.value)


def _node_lookup(noun_entity: NounEntity):
    subject = noun_entity.to_var()

    if subject.startswith("dbr:"):
        target = noun_entity.compound_noun

        if noun_entity.is_named_entity:
            result = LookupService.entities_lookup(target)
            return RDFClass(
                pydash.get(result, ["0", "resource", "0"], None),
                pydash.get(result, ["0", "type"], []),
                pydash.get(result, ["0", "label", "0"], None)
            )
        else:
            resource_name = target.text.title().replace(WORD_SEPARATOR, "_")
            # E.g.: "Where is Fort Knox located?"
            resource = LookupService.resource_lookup(resource_name)

            if resource is None:
                result = LookupService.noun_chunk_lookup(target)
                resource = RDFClass(
                    pydash.get(result, ["0", "resource", "0"], None),
                    pydash.get(result, ["0", "type"], []),
                    pydash.get(result, ["0", "label", "0"], None)
                )

            return resource

    return subject


def _prepare_predicate(subject: Union[str, RDFClass], raw_predicate:  Union[str, Token]):
    predicate = ""

    if isinstance(subject, RDFClass) and isinstance(raw_predicate, Token):
        resource = str(subject)
        return LookupService.property_lookup("Queen_Victoria", raw_predicate, None)

    return predicate
