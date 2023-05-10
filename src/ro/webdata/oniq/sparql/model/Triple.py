import re
from typing import Union

from spacy.tokens import Token

from ro.webdata.oniq.sparql.model.NounEntity import NounEntity

VARNAME_SEPARATOR = "_"


class Triple:
    def __init__(self, s: Union[NounEntity, Token], p: Union[str, Token], o: Union[str, NounEntity, Token]):
        self.s = s if isinstance(s, NounEntity) else NounEntity(s)
        self.p = p
        self.o = _prepare_object(p, o)

    def __eq__(self, other):
        # only equality tests to other 'Triple' instances are supported
        if not isinstance(other, Triple):
            return NotImplemented
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        s = self.s.to_var()
        p = _get_p_var(self.p)
        o = self.o.to_var()

        return f"{s}   {p}   {o}"

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


def _get_p_var(predicate: Union[str, Token]):
    p = predicate if isinstance(predicate, str) else str(predicate)
    return re.sub(r"\s", VARNAME_SEPARATOR, p)


def _prepare_object(predicate: Union[str, Token], obj: Union[str, NounEntity, Token]):
    if isinstance(predicate, str) and predicate == "rdf:type":
        return NounEntity(obj.text, obj.token, True)

    if isinstance(obj, NounEntity):
        return obj

    return NounEntity(obj)
