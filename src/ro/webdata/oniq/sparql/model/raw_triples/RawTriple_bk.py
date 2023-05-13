from typing import Union

import pydash
from spacy.tokens import Span, Token

from ro.webdata.oniq.common.text_utils import WORD_SEPARATOR
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.endpoint.models.RDFElement import RDFClass
from ro.webdata.oniq.endpoint.namespace import NAMESPACE_SEPARATOR
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity

_STRING_SEPARATOR = "_"
_VARIABLE_PREFIX = "?"


class Triple:
    def __init__(self, subject: Union[Span, Token], action: Token, obj: Union[Span, Token] = None, result_type: str = None):
        self.s = TripleSubject(subject)
        self.p = TriplePredicate(action, pydash.get(self.s, ["value", "name"]), result_type)
        # self.o = f'{_VARIABLE_PREFIX}' \
        #          f'{pydash.get(self.p, ["value", "ns_label"])}' \
        #          f'{_STRING_SEPARATOR}' \
        #          f'{pydash.get(self.p, ["value", "name"])}'
        self.o = TripleObject(obj, self.p)

    def __str__(self):
        return f'{self.s} {self.p} {self.o}'


class TripleElement:
    def __init__(self):
        self.input = None
        self.value = None

    def __eq__(self, other):
        # only equality tests to other 'TripleElement' instances are supported
        if not isinstance(other, TripleElement):
            return NotImplemented
        return self.value.uri == other.value.uri

    def __hash__(self):
        return hash(self.value.uri)

    def __str__(self):
        if self.value is None:
            return _VARIABLE_PREFIX + pydash.get(self.input, 'text')

        elif isinstance(self.value, str):
            return _VARIABLE_PREFIX + self.value

        ns_label = pydash.get(self.value, "ns_label")
        name = pydash.get(self.value, "name")

        return ns_label + NAMESPACE_SEPARATOR + name


class TripleSubject(TripleElement):
    def __init__(self, subject: Union[Span, Token]):
        super().__init__()
        self.input = subject
        self.value = _get_node_value(subject)

    def __eq__(self, other):
        # only equality tests to other 'TripleSubject' instances are supported
        if not isinstance(other, TripleSubject):
            return NotImplemented
        return self.value.uri == other.value.uri

    def __hash__(self):
        return hash(self.value.uri)


class TriplePredicate(TripleElement):
    def __init__(self, action: Token, subject_name: str, result_type: str = None):
        super().__init__()
        self.input = action
        self.value = LookupService.property_lookup(subject_name, action, result_type)

    def __eq__(self, other):
        # only equality tests to other 'TriplePredicate' instances are supported
        if not isinstance(other, TriplePredicate):
            return NotImplemented
        return self.value.uri == other.value.uri

    def __hash__(self):
        return hash(self.value.uri)


class TripleObject(TripleElement):
    def __init__(self, obj: Union[Span, Token], predicate: TriplePredicate):
        super().__init__()
        self.input = obj
        self.value = _get_node_value(obj, predicate)

    def __eq__(self, other):
        # only equality tests to other 'TripleObject' instances are supported
        if not isinstance(other, TripleObject):
            return NotImplemented
        return self.value.uri == other.value.uri

    def __hash__(self):
        return hash(self.value.uri)


def _get_node_value(subject: Union[Span, Token], predicate: TriplePredicate = None):
    target = subject

    if isinstance(subject, Token):
        target = NounEntity.get_noun_entity(subject)

    if isinstance(target, Span):
        # FIXME:
        is_named_entity = target in list(subject.doc.ents)

        if is_named_entity:
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

    if predicate is None:
        return None

    return f'{pydash.get(predicate, ["value", "ns_label"])}' \
           f'{_STRING_SEPARATOR}' \
           f'{pydash.get(predicate, ["value", "name"])}'
