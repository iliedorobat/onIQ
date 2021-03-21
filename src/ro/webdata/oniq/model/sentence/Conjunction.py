from typing import Union
from spacy.tokens import Token


class CONJUNCTION_TYPE:
    AND = "and"
    COMMA = ","
    OR = "or"


class Conjunction:
    """
    The conjunction ("and", "or", ",")

    :attr conj: The target token
    :attr default: A default value that will be used if the conjunction == ","
    """

    def __init__(self, conj: Token = None):
        self.token = conj
        self._meta_token = None
        self.text = _prepare_text(conj)

    def __eq__(self, other):
        if not isinstance(other, Conjunction):
            return NotImplemented
        return other is not None \
            and self.token == other.token \
            and self.text == other.text

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}{self.text}'
        )

    @property
    def meta_token(self):
        return self._meta_token

    @meta_token.setter
    def meta_token(self, value):
        self._meta_token = value
        self.text = _prepare_text(self._meta_token)


def _prepare_text(conj: Token):
    """
    Prepare the text which will be displayed

    :param conj: The target token
    :return: The text
    """

    if conj is None:
        return None

    if conj.pos_ == "PUNCT" and conj.text == ",":
        return CONJUNCTION_TYPE.COMMA
    elif conj.lower_ == CONJUNCTION_TYPE.AND:
        return CONJUNCTION_TYPE.AND
    elif conj.lower_ == CONJUNCTION_TYPE.OR:
        return CONJUNCTION_TYPE.OR
    return None
