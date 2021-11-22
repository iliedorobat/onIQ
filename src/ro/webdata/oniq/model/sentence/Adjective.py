from spacy.tokens import Token
from ro.webdata.oniq.nlp.adv_utils import get_comparison_adv
from ro.webdata.oniq.nlp.word_utils import is_adj


class Adjective:
    """
    Data structure for representing an adjective

    :attr token: The token which represents the adjectival complement
    :attr comparison_adv: The superlative/comparative adverb that precedes the adjective

    E.g.:
        - sentence: "Which is the most beautiful city?"
            - token: "beautiful"
            - comparison_adv: "most"
    """

    def __init__(self, word: Token = None):
        self.token = word \
            if word is not None and is_adj(word) \
            else None
        self.comparison_adv = get_comparison_adv(self.token)

    def __eq__(self, other):
        if not isinstance(other, Adjective):
            return NotImplemented
        return other is not None and \
            self.token == other.token

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        adj = self.token if self else None

        return (
            f'{indentation}{adj}'
        )

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
