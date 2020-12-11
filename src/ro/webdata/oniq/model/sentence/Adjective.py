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
        - prefix: "most"
    """

    def __init__(self, sentence: Span, word: Token = None):
        self.adj = _get_adj(word)
        self.prefix = _get_prefix(sentence, self.adj)

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        adj = self.adj if self else None
        prefix = self.prefix if self else None
        full_adj = f'{prefix} {adj}' if prefix is not None else adj

        return (
            f'{indentation}{full_adj}'
        )


def _get_adj(word: Token = None):
    """
    Get the adjective if has syntactic dependency of adjectival modifier (amod)
    or get the noun if has syntactic dependency of attribute (attr)

    :param word: The target adjective or noun
    :return: The amod or the attr
    """

    if word is None:
        return None

    #                                                E.g.: "is married", "the noisiest"
    if (word.pos_ == "ADJ" and word.dep_ == "amod") or (word.pos_ == "NOUN" and word.dep_ == "attr"):
        return word
    return None


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
