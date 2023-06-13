import re
from typing import Union

from spacy.tokens import Span, Token

from ro.webdata.oniq.sparql.constants import SPARQL_STR_SEPARATOR
from ro.webdata.oniq.sparql.model.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.model.NLQuestion import QUESTION_TARGET
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity


class RawTriple:
    def __init__(self, s: Union[str, NounEntity, Token], p: Union[str, Span], o: Union[str, AdjectiveEntity, NounEntity, Token], question: Span, order_modifier: str = None):
        self.s = s if isinstance(s, NounEntity) else NounEntity(s)
        self.p = p
        self.o = _prepare_object(self.p, o)
        self.order_modifier = order_modifier
        self.question = question

    def __eq__(self, other):
        # only equality tests to other 'RawTriple' instances are supported
        if not isinstance(other, RawTriple):
            return NotImplemented
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        s = self.s.to_var()
        p = _get_p_var(self.p)
        o = self.o.to_var()

        return f"{s}   {p}   {o}"

    def is_ordering_triple(self):
        return self.order_modifier is not None

    def is_valid(self):
        validation = True

        if self.s.to_var() == "NULL":
            print("The Subject is NULL")
            validation = False
        if self.o.to_var() == "NULL":
            print("The Object is NULL")
            validation = False
        if self.p is None:
            print("The Predicate is NULL")
            validation = False

        return validation

    def is_location(self):
        return str(self.p) == QUESTION_TARGET.LOCATION

    def is_rdf_type(self):
        return str(self.p) == "rdf:type"

    def is_dbo_mountain_type(self):
        return self.is_rdf_type() and self.o.to_var() == "dbo:Mountain"


def _get_p_var(predicate: Union[str, Token]):
    p = predicate if isinstance(predicate, str) else str(predicate)
    return re.sub(r"\s", SPARQL_STR_SEPARATOR, p)


def _prepare_object(predicate: Union[str, Span], obj: Union[str, AdjectiveEntity, NounEntity, Token]):
    if isinstance(predicate, str) and predicate == "rdf:type":
        return NounEntity(obj.text, obj.token, True)

    if isinstance(obj, NounEntity):
        return obj

    if isinstance(obj, AdjectiveEntity):
        return obj

    return NounEntity(obj)
