from spacy.tokens import Token
from ro.webdata.oniq.nlp.word_utils import is_adv


class Adverb:
    """
    Data structure for representing an adverb

    :attr token: The token which represents the adverb

    E.g.:
        - sentence: "How many cars are there?"
            - token: "there"
    """

    def __init__(self, word: Token = None):
        self.token = word \
            if word is not None and is_adv(word) \
            else None

    def __eq__(self, other):
        if not isinstance(other, Adverb):
            return NotImplemented
        return other is not None and \
            self.token == other.token

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        adverb = self.token if self else None

        return (
            f'{indentation}{adverb}'
        )
