from spacy.tokens import Token

from ro.webdata.oniq.sparql.NounEntity import NounEntity


class COMPARISON_OPERATORS:
    CONTAINS = 'contains'
    NOT_CONTAINS = '!contains'
    REGEX = 'regex'
    EQ = '='
    NOT_EQ = '!='
    GT = '>'
    GTE = '>='
    LT = '<'
    LTE = '<='


# TODO: date-like
class FILTER_FUNCTION:
    YEAR = "year"


class Filter:
    def __init__(self, target: NounEntity, value: Token, operator: str, filter_type: str):
        self.filter_type = filter_type
        self.operator = operator
        self.target = target
        self.value = value

    def __str__(self):
        if self.filter_type == FILTER_FUNCTION.YEAR:
            if not self.is_empty():
                if self.target.is_var():
                    output = "FILTER ("
                    output += f"{FILTER_FUNCTION.YEAR}({self.target.to_var()}) "
                    output += f"{self.operator} "
                    output += f"{self.value}"
                    output += ")"

                    return output
        return None

    def is_empty(self):
        return self.operator is None or self.target is None or self.value is None
