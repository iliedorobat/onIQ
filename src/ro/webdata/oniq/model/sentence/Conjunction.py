from typing import Union
from spacy.tokens import Token


class CONJUNCTION_TYPE:
    AND = 'and'
    OR = 'or'


class Conjunction:
    """
    The conjunction ("and", "or", ",")

    :attr conj: The target token
    :attr default: A default value that will be used if the conjunction == ","
    """

    # TODO: default: Union[CONJUNCTION_TYPE.AND, CONJUNCTION_TYPE.OR]
    def __init__(self, conj: Token = None, default=None):
        self.conj = conj
        self.text = _prepare_text(conj, default)

    def __eq__(self, other):
        if not isinstance(other, Conjunction):
            return NotImplemented
        return other is not None \
            and self.conj == other.conj \
            and self.text == other.text

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}{self.text}'
        )


def _prepare_text(conj: Token, default: Token):
    """
    Prepare the text which will be displayed

    :param conj: The target token
    :param default: CONJUNCTION_TYPE.AND or CONJUNCTION_TYPE.OR
    :return: The text
    """

    if conj is None:
        return None

    if conj.pos_ == "PUNCT" and conj.text == ",":
        if default is not None:
            return default
        return CONJUNCTION_TYPE.AND
    elif conj.lower_ == CONJUNCTION_TYPE.AND:
        return CONJUNCTION_TYPE.AND
    elif conj.lower_ == CONJUNCTION_TYPE.OR:
        return CONJUNCTION_TYPE.OR
    return None
