from spacy.tokens import Span, Token


class Adjective:
    """
    Data structure for representing an adjective

    :attr sentence: The target sentence
    :attr token: The token which represents the adjectival complement
    :attr prefix: The prefix of the superlative/comparative adjective

    E.g.:
        - sentence: "Which is the most beautiful city?"
        - adj: "beautiful"
        - det: "the"
        - prefix: "most"
    """

    def __init__(self, sentence: Span, word: Token = None):
        self.token = _get_acomp_token(word)
        self.det = _get_determiner(sentence, self.token)
        self.prefix = _get_prefix(sentence, self.token)

    def __eq__(self, other):
        if not isinstance(other, Adjective):
            return NotImplemented
        return other is not None and \
            self.token == other.token and \
            self.det == other.det and \
            self.prefix == other.prefix

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        token = self.token if self else None
        det = self.det if self else None
        prefix = self.prefix if self else None
        full_adj = f'{prefix} {token}' if prefix is not None else token
        full_adj = f'{det} {full_adj}' if det is not None else full_adj

        return (
            f'{indentation}{full_adj}'
        )

    def to_list(self):
        adj_list = [self.token, self.det, self.prefix]
        return [token for token in adj_list if token is not None]

    @staticmethod
    def get_first_token(adjective):
        if adjective.det is not None:
            return adjective.det
        elif adjective.prefix is not None:
            return adjective.prefix
        else:
            return adjective.token

    @staticmethod
    def get_first_index(adjective):
        first_token = Adjective.get_first_token(adjective)
        if first_token is not None:
            return first_token.i
        else:
            return -1


def _get_acomp_token(word: Token = None):
    """
    Get the adjective or get the noun if the latter
    has syntactic dependency of attribute (attr)

    :param word: The target adjective or noun
    :return: The adjective or the attribute
    """

    if word is None:
        return None

    #                        E.g.: "is married", "the noisiest"
    if word.pos_ == "ADJ" or (word.pos_ == "NOUN" and word.dep_ == "attr"):
        return word
    return None


def _get_determiner(sentence: Span, adj: Token = None):
    """
    Get the determiner placed before the adjective

    :param sentence: The target sentence
    :param adj: The main adjective
    :return: The determiner
    """

    if adj is None:
        return None

    prev_index = adj.i - 1

    prefix = _get_prefix(sentence, adj)
    if prefix is not None:
        prev_index = prev_index - 1

    prev_word = sentence[prev_index] if prev_index > -1 else None
    return prev_word if prev_word.pos_ == "DET" and prev_word.tag_ == "DT" else None


def _get_prefix(sentence: Span, adj: Token = None):
    """
    Get the superlative/comparative adjective prefix

    :param sentence: The target sentence
    :param adj: The main adjective
    :return: The superlative/comparative adjective prefix
    """

    if adj is None:
        return None

    prev_word = sentence[adj.i - 1] if adj.i > 0 else None
    return prev_word if prev_word is not None and prev_word.tag_ in ["RBR", "RBS"] else None
