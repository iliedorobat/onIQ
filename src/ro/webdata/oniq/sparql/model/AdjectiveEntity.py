from spacy.tokens import Token

from ro.webdata.oniq.common.nlp.word_utils import is_adj, get_prev_word, is_adv
from ro.webdata.oniq.sparql.constants import SPARQL_VAR_PREFIX


class AdjectiveEntity:
    def __init__(self, word: Token):
        self.adj = None
        self.prev_adv = None
        self.text = None
        self.token = None

        if is_adj(word):
            self.adj = word
            self.prev_adv = _get_prev_adv(word)
            self.text = word.text
            self.token = word

    def __eq__(self, other):
        if not isinstance(other, AdjectiveEntity):
            return NotImplemented
        return self.adj == other.adj

    def __str__(self):
        if self.adj is not None:
            return self.text
        elif self.text is not None:
            return self.text
        else:
            return "NULL"

    def is_null(self):
        return str(self) == "NULL"

    def is_res(self):
        return "dbr:" in self.to_var()

    def is_var(self):
        return SPARQL_VAR_PREFIX in self.to_var()

    def to_var(self):
        if self.adj is not None:
            return f"{SPARQL_VAR_PREFIX}{self.text}"


def _get_prev_adv(word: Token):
    if not is_adj(word):
        return None

    prev_word = get_prev_word(word)

    if is_adv(prev_word):
        return prev_word

    return None
