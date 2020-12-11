from spacy.tokens import Span, Token


class Adjective:
    """
    Data structure for representing an adjective

    :attr sentence: The target sentence
    :attr adj: The main adjective
    :attr prefix: The prefix of the superlative/comparative adjective

    E.g.:
        - sentence: "Which is the most beautiful city?"
        - adj: "beautiful"
        - det: "the"
        - prefix: "most"
    """

    def __init__(self, sentence: Span, word: Token = None):
        self.adj = _get_adj(word)
        self.det = _get_determiner(sentence, self.adj)
        self.prefix = _get_prefix(sentence, self.adj)

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        adj = self.adj if self else None
        det = self.det if self else None
        prefix = self.prefix if self else None
        full_adj = f'{prefix} {adj}' if prefix is not None else adj
        full_adj = f'{det} {full_adj}' if det is not None else full_adj

        return (
            f'{indentation}{full_adj}'
        )


def _get_adj(word: Token = None):
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
