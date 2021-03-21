from typing import Union
from spacy.tokens import Doc, Span, Token
from ro.webdata.oniq.model.sentence.Conjunction import Conjunction
from ro.webdata.oniq.nlp.word_utils import get_preposition, get_word_before_prep, is_conjunction, is_wh_word


class PHRASES_TYPES:
    HOW = "how"
    WHAT = "what"
    WHEN = "when"
    WHERE = "where"
    WHICH = "which"
    WHO = "who"
    WHOM = "whom"
    WHOSE = "whose"
    WHY = "why"


class Phrase:
    """
    A sentence that also contains the preposition of the target chunk

    :attr chunk: The target chunk
    :attr conj: The conjunction
    :attr prep: The preposition of the phrase
    :attr meta_prep: The preposition of the previous related phrase
    :attr content: The content of the phrase
    :attr text: The text
    :attr type: The type of the phrase (one of PHRASES_TYPES values)
    :attr start: The index of the first token that composes the phrase
    :attr end: The index of the last token that composes the phrase
    """

    def __init__(self, sentence: Span, chunk_list: [Span], index: int):
        self._sentence = sentence
        self.chunk = chunk_list[index]
        self.conj = _prepare_conjunction(sentence, self.chunk)
        self.prep = _prepare_preposition(sentence, self.chunk)
        self._meta_prep = None
        self.content = _prepare_content(sentence, self.chunk, self.prep)
        self.type = _prepare_type(sentence, chunk_list, index, self.conj)
        self.text = _prepare_text(sentence, self.chunk, self.prep, self._meta_prep, self.type)
        self.start = self.content.start if self.content is not None else -1
        self.end = self.content[len(self.content) - 1].i if self.content is not None else -1

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
    def meta_prep(self):
        return self._meta_prep

    @meta_prep.setter
    def meta_prep(self, value):
        self._meta_prep = value
        self.text = _prepare_text(self._sentence, self.chunk, self.prep, self._meta_prep, self.type)


def _prepare_conjunction(sentence: Union[Doc, Span], chunk: Span):
    """
    Prepare the conjunction

    :param sentence: The target sentence
    :param chunk: The current iterated chunk
    :return: Conjunction object
    """

    main_word = chunk.root
    # TODO: remove
    # # E.g.: "Which female actor played in Casablanca and has been married to a writer?"
    # # conj(played, married)
    # if main_word.dep_ == "pobj":
    #     main_word = get_word_before_prep(sentence, chunk.root) \

    if main_word.dep_ == "conj":
        last_index = main_word.i

        for i in reversed(range(0, last_index + 1)):
            prev_index = i - 1
            if prev_index < 0:
                return Conjunction()

            prev_word = sentence[prev_index]
            # E.g.: "Which paintings, swords and statues have not been deposited in Bacau?"
            # E.g.: "Which is the noisiest and the largest city?"
            # E.g.: "What museums are in Bacau, Iasi or Bucharest?"
            if is_conjunction(prev_word):
                return Conjunction(prev_word)

    return Conjunction()


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


def _prepare_text(sentence: Span, content, prep, meta_prep, phrase_type):
    """
    Prepare the text which will be displayed

    :param sentence: The target sentence
    :param content: The content of the phrase
    :param prep: The preposition of the phrase
    :param meta_prep: The preposition of the previous related phrase
    :param phrase_type: The type of the phrase
    :return: The text
    """

    if prep is not None:
        return f'{prep} {content}'
    if meta_prep is not None:
        return f'{meta_prep} {content}'

    first_index = content.start
    text = sentence[first_index: content.end]

    if is_wh_word(content[0]):
        # E.g.: "What is the name of the largest museum?"
        if len(content) == 1:
            return phrase_type
        # Exclude the WH-word from the displayed text
        elif len(content) > 1:
            first_index = first_index + 1
            text = sentence[first_index: content.end]

    if phrase_type is not None:
        return f'{phrase_type} {text}'

    return f'{text}'


def _prepare_type(sentence: Span, chunk_list: [Span], index: int, conj):
    """
    Extract the type of the phrase

    :param sentence: The target sentence
    :param chunk_list: The list of chunks
    :param index: The index of the current iterated chunk
    :param conj: The conjunction
    :return: One of PHRASES_TYPES values
    """

    chunk = chunk_list[index]
    first_word = chunk[0].lower_
    if first_word in PHRASES_TYPES.__dict__.values():
        return first_word

    if conj.token is not None:
        prev_phrase = chunk_list[index - 1]
        prev_conj = _prepare_conjunction(sentence, prev_phrase)
        return _prepare_type(sentence, chunk_list, index - 1, prev_conj)

    return None
