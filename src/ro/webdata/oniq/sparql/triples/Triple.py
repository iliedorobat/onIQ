from typing import Union, List

from spacy.tokens import Span

from ro.webdata.oniq.common.nlp.word_utils import is_aux, is_preposition, is_adj
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.endpoint.query import escape_resource_name
from ro.webdata.oniq.service.query_const import NODE_TYPE
from ro.webdata.oniq.sparql.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.NounEntity import NounEntity
from ro.webdata.oniq.sparql.common.SpotlightService import SpotlightService
from ro.webdata.oniq.sparql.triples.raw_triples.RawTriple import RawTriple


class Triple:
    def __init__(self, raw_triple: RawTriple, raw_triples_values: List[RawTriple], properties: RDFElements):
        self.s = raw_triple.s
        self.p = _predicate_lookup(raw_triple, raw_triples_values, properties)
        self.o = raw_triple.o
        self.question = raw_triple.question
        self.order_by = raw_triple.order_by

    def __eq__(self, other):
        # only equality tests to other 'Triple' instances are supported
        if not isinstance(other, Triple):
            return NotImplemented
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        if self.s.text == "VALUES":
            # E.g.: "Who is Dan Jurafsky?"
            return f"{str(self.s)}   ?{str(self.p)}   {{ {self.o.to_var()} }}"

        if self.p is None:
            return None

        if isinstance(self.p, PropertyMatcher):
            p = str(self.p.property)
        else:
            p = self.p

        s = self.s.to_var()
        o = self.o.to_var()

        return f"{s}   {p}   {o}"

    def is_ordering_triple(self):
        return self.order_by is not None

    def to_escaped_str(self):
        if self.s.text == "VALUES":
            # E.g.: "Who is Dan Jurafsky?"
            return f"{str(self.s)}   ?{str(self.p)}   {{ {self.o.to_var()} }}"

        if self.p is None:
            return None

        if isinstance(self.p, PropertyMatcher):
            p = str(self.p.property)
        else:
            p = self.p

        s = escape_resource_name(
            self.s.to_var()
        )
        o = escape_resource_name(
            self.o.to_var()
        )

        return f"{s}   {p}   {o}"


def _predicate_lookup(raw_triple: RawTriple, raw_triples_values: List[RawTriple], properties: RDFElements):
    subject: NounEntity = raw_triple.s
    predicate: Union[str, Span] = raw_triple.p
    obj: Union[AdjectiveEntity, NounEntity] = raw_triple.o
    question: Span = raw_triple.question

    if predicate is None:
        # TODO: check "Who is the mayor of Rotterdam?"
        return None

    if subject.text == "VALUES":
        # E.g.: "Who is Dan Jurafsky?"
        return predicate

    if isinstance(predicate, PropertyMatcher):
        # E.g.: "Which museum in New York has the most visitors?"
        return predicate

    if isinstance(predicate, Span):
        if is_aux(predicate.root):
            # TODO: move the logic to RawTriples
            if predicate.root.lemma_ == "have":
                # E.g. "Which museum in New York has the most visitors?"
                if subject.is_var() and obj.is_var():
                    predicate = obj.to_span()
            else:
                return "?property"

    if isinstance(predicate, Span) and is_adj(predicate.root):
        return SpotlightService.adj_property_lookup(predicate, properties)

    if subject.is_res():
        if obj.is_var():
            # E.g.: "In which country is Mecca located?"
            return SpotlightService.property_lookup(
                question=question,
                predicate=predicate,
                node_type=NODE_TYPE.SUBJECT,
                node_value=subject,
                raw_triples_values=raw_triples_values
            )

    if subject.is_var():
        # E.g.: "Give me all Swedish holidays."
        # E.g.: "Who is the youngest Pulitzer Prize winner?"
        return SpotlightService.property_lookup(
            question=question,
            predicate=predicate,
            node_type=NODE_TYPE.OBJECT,
            node_value=obj,
            raw_triples_values=raw_triples_values
        )

    # E.g.: "Who is the tallest basketball player?"
    return predicate
