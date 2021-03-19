from spacy.tokens import Span, Token


class Phrase:
    """
    A sentence that also contains the preposition of the target chunk

    :attr chunk: The target chunk
    :attr prep: The preposition of the phrase
    :attr meta_prep: The preposition of the previous related phrase
    :attr content: The content of the phrase
    :attr is_target: Specify whether or not a is target phrase
    :attr text: The text
    :attr i: The index of the first token that composes the phrase
    :attr last_i: The index of the last token that composes the phrase
    """

    def __init__(self, sentence: Span, chunk: Span, is_target: bool = False):
        self.chunk = chunk
        self.prep = _prepare_preposition(sentence, chunk)
        self._meta_prep = None
        self.content = _prepare_content(sentence, self.chunk, self.prep)
        self._is_target = is_target
        self.text = _prepare_text(self.chunk, self.prep, self._meta_prep, self._is_target)
        self.i = self.content[0].i if self.content is not None else -1
        self.last_i = chunk[len(self.content) - 1].i if self.content is not None else -1

    def __eq__(self, other):
        if not isinstance(other, Phrase):
            return NotImplemented
        return other is not None and \
            self.prep == other.prep and \
            self.chunk == other.chunk

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
        self.text = _prepare_text(self.chunk, self.prep, self._meta_prep, self._is_target)

    @meta_prep.setter
    def meta_prep(self, value):
        self._meta_prep = value
        self.text = _prepare_text(self.chunk, self.prep, self._meta_prep, self._is_target)


def _prepare_content(sentence: Span, chunk: Span, prep: Token):
    """
    Prepare the content of the phrase

    :param sentence: The target sentence
    :param chunk: The target chunk
    :param prep: The preposition of the phrase
    :return: The content of the phrase
    """

    first_index = prep.i if prep is not None else chunk[0].i
    last_index = chunk[len(chunk) - 1].i + 1
    return sentence[first_index: last_index]


def _prepare_preposition(sentence: Span, chunk: Span):
    """
    Prepare the preposition of the chunk

    :param sentence: The target sentence
    :param chunk: The target chunk
    :return: The preposition of the chunk
    """

    first_index = chunk[0].i
    prev_word = sentence[first_index - 1] if first_index > 0 else None

    # E.g.: "What museums are in Bacau or in Bucharest?"
    # - dep_ == "prep" => "in Bacau"
    # - dep_ == "conj" => "in Bucharest"
    if prev_word is not None and prev_word.pos_ == "ADP" and prev_word.dep_ in ["conj", "prep"]:
        return prev_word

    return None


def _prepare_text(content, prep, meta_prep, is_target):
    """
    Prepare the text which will be displayed

    :param content: The content of the phrase
    :param prep: The preposition of the phrase
    :param meta_prep: The preposition of the previous related phrase
    :param is_target: Specify whether or not a is target phrase
    :return: The text
    """

    if is_target is True:
        return f'{content}'
    if prep is not None:
        return f'{prep} {content}'
    if meta_prep is not None:
        return f'{meta_prep} {content}'
    return f'{content}'
