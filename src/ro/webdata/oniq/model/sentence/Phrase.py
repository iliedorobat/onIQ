from spacy.tokens import Span
from ro.webdata.oniq.nlp.nlp_utils import get_preposition


# TODO: documentation
class Phrase:
    def __init__(self, sentence: Span, chunk: Span, is_target: bool = False):
        self.main_content = chunk
        self.prep = get_preposition(sentence, chunk)  # TODO: check
        self._meta_prep = None
        self.content = _get_content(sentence, self.main_content, self.prep)
        self._is_target = is_target
        self.text = _get_text(self.main_content, self.prep, self._meta_prep, self._is_target)

    def __eq__(self, other):
        if not isinstance(other, Phrase):
            return NotImplemented
        return other is not None and \
            self.prep == other.prep and \
            self.main_content == other.main_content

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}{self.text}'
        )

    @property
    def is_target(self):
        return self._is_target

    @property
    def meta_prep(self):
        return self._meta_prep

    @is_target.setter
    def is_target(self, value):
        self._is_target = value
        self.text = _get_text(self.main_content, self.prep, self._meta_prep, self._is_target)

    @meta_prep.setter
    def meta_prep(self, value):
        self._meta_prep = value
        self.text = _get_text(self.main_content, self.prep, self._meta_prep, self._is_target)


def _get_content(sentence, main_content, prep):
    first_index = prep.i if prep is not None else main_content[0].i
    last_index = main_content[len(main_content) - 1].i + 1
    return sentence[first_index: last_index]


def _get_text(content, prep, meta_prep, is_target):
    if is_target is True:
        return f'{content}'
    if prep is not None:
        return f'{prep} {content}'
    if meta_prep is not None:
        return f'{meta_prep} {content}'
    return f'{content}'
