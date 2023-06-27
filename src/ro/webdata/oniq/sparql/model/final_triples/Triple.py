from typing import Union, List

from spacy.tokens import Span

from ro.webdata.oniq.common.nlp.word_utils import is_aux, is_preposition, is_adj
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.endpoint.query import escape_resource_name
from ro.webdata.oniq.sparql.model.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.final_triples.predicate_utils import subject_predicate_lookup, \
    object_predicate_lookup, adjective_property_lookup
from ro.webdata.oniq.sparql.model.triples.RawTriple import RawTriple


class Triple:
    def __init__(self, raw_triple: RawTriple, raw_triples: List[RawTriple], properties: RDFElements):
        self.s = raw_triple.s
        self.p = _predicate_lookup(raw_triple, raw_triples, properties)
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


def _predicate_lookup(raw_triple: RawTriple, raw_triples: List[RawTriple], properties: RDFElements):
    subject: NounEntity = raw_triple.s
    predicate: Union[str, Span] = raw_triple.p
    obj: Union[AdjectiveEntity, NounEntity] = raw_triple.o
    question: Span = raw_triple.question

    if isinstance(predicate, Span):
        if is_aux(predicate.root):
            if predicate.root.lemma_ == "have":
                # E.g. "Which museum in New York has the most visitors?"
                if subject.is_var() and obj.is_var():
                    predicate = obj.to_span()
            else:
                return "?property"
        elif is_preposition(predicate.root):
            # E.g.: "Which museum in New York has the most visitors?"
            # TODO:
            pass

    if isinstance(predicate, Span) and is_adj(predicate.root):
        return adjective_property_lookup(predicate, properties)

    if subject.is_res():
        if obj.is_var():
            return subject_predicate_lookup(question, subject, predicate, raw_triples)

    if subject.is_var():
        return object_predicate_lookup(question, obj, predicate, raw_triples)

    # E.g.: "Who is the tallest basketball player?"
    #       <?person   rdf:type   dbo:BasketballPlayer>
    return predicate
