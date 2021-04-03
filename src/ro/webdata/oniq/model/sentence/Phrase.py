from typing import Union
from spacy.tokens import Doc, Span, Token

from ro.webdata.oniq.model.sentence.Conjunction import Conjunction
from ro.webdata.oniq.nlp.nlp_utils import get_chunk, get_noun_chunks
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
    :attr text: The text
    :attr type: The type of the phrase (one of PHRASES_TYPES values)
    """

    def __init__(self, sentence: Span, chunk: Span):
        self.chunk = chunk
        self.conj = _prepare_conjunction(sentence, self.chunk)
        self.prep = get_preposition(sentence, self.chunk.root)
        self.meta_prep = _prepare_meta_prep(sentence, self.chunk)
        self.type = _prepare_type(sentence, self.chunk)
        self.text = _prepare_text(self.chunk, self.prep, self.meta_prep, self.type)

    def __eq__(self, other):
        if not isinstance(other, Phrase):
            return NotImplemented
        return other is not None and \
            self.chunk == other.chunk and \
            self.conj == other.conj and \
            self.prep == other.prep

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}{self.text}'
        )


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

    # E.g.: "Which woman is beautiful, generous, tall and sweet?"   => generous.dep_ == "intj"
    if main_word.dep_ in ["conj", "intj"]:
        last_index = main_word.i

        for i in reversed(range(0, last_index + 1)):
            prev_index = i - 1
            if prev_index < 0:
                return None

            prev_word = sentence[prev_index]
            # E.g.: "Which paintings, swords and statues have not been deposited in Bacau?"
            # E.g.: "Which is the noisiest and the largest city?"
            # E.g.: "What museums are in Bacau, Iasi or Bucharest?"
            if is_conjunction(prev_word):
                return Conjunction(prev_word)

    return None


# TODO: documentation
def _prepare_meta_prep(sentence: Span, chunk: Span):
    prep = get_preposition(sentence, chunk.root)

    # Return "None" if the chunk has its own preposition
    if prep is not None:
        return None

    for token in chunk.conjuncts:
        prep = get_preposition(sentence, token)
        if prep is not None:
            return prep

    return None


def _prepare_text(chunk: Span, prep: Token, meta_prep: Token, phrase_type: PHRASES_TYPES):
    """
    Prepare the text which will be displayed

    :param chunk: The target chunk
    :param prep: The preposition of the phrase
    :param meta_prep: The preposition of the previous related phrase
    :param phrase_type: The type of the phrase
    :return: The text
    """

    text = chunk.text

    if prep is not None:
        return f'{prep} {text}'
    if meta_prep is not None:
        return f'{meta_prep} {text}'

    # Exclude the WH-word
    if is_wh_word(chunk[0]):
        text = chunk[chunk.start + 1: chunk.end].text

    if phrase_type is not None:
        return f'{phrase_type} {text}'.strip()

    return f'{text}'


def _prepare_type(sentence: Span, chunk: Span):
    """
    Extract the type of the phrase

    :param chunk: The target chunk
    :return: One of PHRASES_TYPES values
    """

    chunk_list = get_noun_chunks(sentence)
    conjuncts = [chunk.root] + list(chunk.conjuncts)

    for token in conjuncts:
        chunk = get_chunk(chunk_list, token)
        first_word = chunk[0].lower_ if chunk is not None else None
        if first_word in PHRASES_TYPES.__dict__.values():
            return first_word

    return None
