import re
from typing import Union

from spacy.tokens import Span, Token

from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.query import escape_resource_name
from ro.webdata.oniq.sparql.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.NounEntity import NounEntity
from ro.webdata.oniq.sparql.common.constants import SPARQL_STR_SEPARATOR
from ro.webdata.oniq.sparql.order.OrderBy import OrderBy


class RawTriple:
    def __init__(self, s: Union[str, NounEntity, Token], p: Union[str, Span], o: Union[str, AdjectiveEntity, NounEntity, Token], question: Span, order_by: OrderBy = None):
        self.s = s if isinstance(s, NounEntity) else NounEntity(s)
        self.p = p
        self.o = _prepare_object(o)
        self.order_by = order_by
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
        return self.order_by is not None

    def is_valid(self):
        validation = True

        if self.s.to_var() == "NULL":
            print("The Subject is NULL")
            validation = False
        if self.p is None:
            print("The Predicate is NULL")
            validation = False
        if self.o.to_var() == "NULL":
            print("The Object is NULL")
            validation = False

        return validation

    def to_escaped_str(self, append_prefix: bool = False):
        if self.p is None:
            return None

        if isinstance(self.p, PropertyMatcher):
            p = str(self.p.property)
        elif self.is_rdf_type() or self.is_dbpedia_prop():
            p = self.p
        else:
            p = "?property"
            if append_prefix is True:
                p = f"?p_{self.p}"

        s = escape_resource_name(
            self.s.to_var()
        )

        o = escape_resource_name(
            self.o.to_var()
        )

        return f"{s}   {p}   {o}"

    def is_dbpedia_prop(self):
        if not isinstance(self.p, str):
            return False
        return self.p.startswith("dbo:") or self.p.startswith("dbr:")

    def is_rdf_type(self):
        return str(self.p) == "rdf:type"

    def is_dbo_mountain_type(self):
        return self.is_rdf_type() and self.o.to_var() == "dbo:Mountain"


def _get_p_var(predicate: Union[str, Token]):
    p = predicate if isinstance(predicate, str) else str(predicate)
    return re.sub(r"\s", SPARQL_STR_SEPARATOR, p)


def _prepare_object(obj: Union[str, AdjectiveEntity, NounEntity, Token]):
    if isinstance(obj, NounEntity):
        return obj

    if isinstance(obj, AdjectiveEntity):
        return obj

    return NounEntity(obj)
