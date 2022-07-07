from spacy.tokens import Token


class CONJUNCTION_TYPE:
    AND = "and"
    COMMA = ","
    OR = "or"


class Conjunction:
    """
    The conjunction ("and", "or", ",")

    :attr token: The target token
    :attr meta_token: TODO: doc
    :attr text: TODO: doc
    """

    def __init__(self, conj: Token = None):
        self.token = conj
        self._meta_token = _get_meta_token(self.token)
        self.text = _prepare_text(self.token, self.meta_token)

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
        self.text = _prepare_text(self.token, self._meta_token)


def _prepare_text(token: Token, meta_token: Token):
    """
    Prepare the text which will be displayed

    :param token: The target token
    :param meta_token: The related conjunction
    :return: The text
    """

    conj = meta_token if meta_token is not None else token

    if not isinstance(conj, Token):
        return None

    if conj.lower_ == CONJUNCTION_TYPE.AND:
        return CONJUNCTION_TYPE.AND
    elif conj.lower_ == CONJUNCTION_TYPE.OR:
        return CONJUNCTION_TYPE.OR

    return None


# TODO: ilie.doroabt: add the documentation
# E.g.: "Which woman is beautiful, generous, tall and rich?"
def _get_meta_token(word: Token):
    if not isinstance(word, Token) or word.pos_ == "CCONJ":
        return None

    sentence = word.sent

    for index in range(word.i, len(sentence)):
        token = sentence[index]
        if token.pos_ == "CCONJ":
            return token

    return None
