from typing import Union
from spacy.tokens import Doc, Span, Token

from ro.webdata.oniq.common.constants import QUESTION_TYPES
from ro.webdata.oniq.model.sentence.Conjunction import Conjunction
from ro.webdata.oniq.nlp.chunk_utils import extract_comparison_adv, extract_determiner
from ro.webdata.oniq.nlp.nlp_utils import get_noun_chunks, get_chunk_index
from ro.webdata.oniq.nlp.utils import is_empty_list
from ro.webdata.oniq.nlp.word_utils import get_preposition, is_adj, is_conjunction, \
    is_followed_by_conjunction, is_preceded_by_conjunction, is_verb, is_wh_word


class PHRASE_TYPES:
    RELATED = "related"
    TARGET = "target"


class Phrase:
    """
    A sentence that also contains the preposition of the target chunk

    :attr chunk: The target chunk
    :attr conj: The conjunction
    :attr prep: The preposition of the phrase
    :attr meta_prep: The preposition of the previous related phrase
    :attr phrase_type: The type of the phrase (one of PHRASE_TYPES values)
    :attr question_type: The type of the question (one of QUESTION_TYPES values)
    :attr text: The text
    """

    def __init__(self, sentence: Span, chunk: Span, phrase_type: str):
        self.chunk = chunk
        self.conj = _prepare_conjunction(sentence, self.chunk)

        self.comparison_adv = extract_comparison_adv(chunk)
        self.det = extract_determiner(self.chunk)
        self.prep = get_preposition(self.chunk.root)
        self.meta_prep = _prepare_meta_prep(self.chunk, self.prep)

        self.phrase_type = phrase_type
        self.question_type = _prepare_question_type(sentence, self.chunk)
        self.text = _prepare_text(self.chunk,  self.comparison_adv, self.det, self.prep, self.meta_prep, self.question_type)

    def __eq__(self, other):
        if not isinstance(other, Phrase):
            return NotImplemented
        return other is not None and \
            self.chunk == other.chunk and \
            self.conj == other.conj and \
            self.prep == other.prep

    def __str__(self):
        return self.get_str(self.phrase_type)

    def get_str(self, phrase_type, indentation=''):
        text = f'##{self.conj}## {self.text}' if self.conj else self.text

        return (
            f'{indentation}{phrase_type}: {{\n'
            f'{indentation}\tphrase: {text}\n'
            f'{indentation}\tquestion type: {self.question_type}\n'
            f'{indentation}}}'
        )


def _prepare_conjunction(sentence: Union[Doc, Span], chunk: Span):
    """
    Prepare the conjunction

    :param sentence: The target sentence
    :param chunk: The current iterated chunk
    :return: Conjunction object
    """

    if sentence is None or len(sentence) == 0:
        return None

    first_word = sentence[0]
    chunk_list = get_noun_chunks(sentence)

    if is_wh_word(first_word):
        main_word = chunk.root
        # E.g.: "Which is the noisiest and the largest city?"
        # E.g.: "Which is the noisiest town and the largest city?"
        if len(chunk_list) == 0:
            if is_followed_by_conjunction(main_word):
                for index in range(main_word.i + 1, len(sentence)):
                    next_token = sentence[index]
                    if is_conjunction(next_token):
                        return Conjunction(next_token)

        # E.g.: "Which paintings, swords and statues have not been deposited in Bacau?"
        # E.g.: "Which paintings, swords or statues are in Bacau?"
        # E.g.: "What museums are in Bacau, Iasi or Bucharest?"
        else:
            main_word = chunk[0]
            if is_preceded_by_conjunction(main_word):
                for index in reversed(range(0, main_word.i)):
                    prev_token = sentence[index]
                    if is_verb(prev_token):
                        return None
                    elif is_conjunction(prev_token):
                        return Conjunction(prev_token)

    return None


def _prepare_meta_prep(chunk: Span, prep: Token):
    """
    Get the meta preposition for the chunk

    E.g.: "What museums and libraries are in Bacau or Bucharest?"
        - phrase_list: ["what museums", "what libraries", "in Bacau", "in Bucharest"]
            - statement 1: "what museums", "are", "in Bacau"
                - "in Bacau" has its own preposition
            - statement 2: "what libraries", "are", "in Bucharest"
                - "in Bucharest" doesn't have its own preposition but it
                 takes a meta preposition (the preposition of "in Bacau")

    :param chunk: The current iterated chunk
    :param prep: The phrase's preposition (or None if not exists)
    :return: The meta preposition (or None if not exists or the phrase has its own preposition)
    """

    # Return "None" if the chunk has its own preposition
    if prep is not None:
        return None

    for token in chunk.conjuncts:
        meta_prep = get_preposition(token)
        if meta_prep is not None:
            return meta_prep

    return None


def _prepare_text(chunk: Span, comparison_adv: Token, det: Token, prep: Token, meta_prep: Token, question_type: QUESTION_TYPES):
    """
    Prepare the text which will be displayed

    :param chunk: The target chunk
    :param prep: The preposition of the phrase
    :param meta_prep: The preposition of the previous related phrase
    :param question_type: The type of the question
    :return: The text
    """

    if not isinstance(chunk, Span):
        return None

    text = chunk.text

    if isinstance(comparison_adv, Token):
        if comparison_adv.text.lower() not in text.lower():
            text = f'{comparison_adv} {text}'

    if isinstance(det, Token):
        if det.text.lower() not in text.lower():
            text = f'{det} {text}'

    if isinstance(prep, Token):
        if prep.text.lower() not in text.lower():
            return f'{prep} {text}'

    if isinstance(meta_prep, Token):
        if meta_prep.text.lower() not in text.lower():
            return f'{meta_prep} {text}'

    # Exclude the WH-word
    if is_wh_word(chunk[0]):
        text = chunk[chunk.start + 1: chunk.end].text

    if isinstance(question_type, str):
        if question_type == QUESTION_TYPES.COUNT:
            return f'{QUESTION_TYPES.HOW} {text}'.strip()
        return f'{question_type} {text}'.strip()

    return f'{text}'


def _prepare_question_type(sentence: Span, chunk: Span):
    """
    Extract the type of the question

    :param chunk: The target chunk
    :return: One of QUESTION_TYPES values
    """

    if not isinstance(sentence, Span) or not isinstance(chunk, Span):
        return None

    chunk_list = get_noun_chunks(sentence)
    first_word = _get_first_word(chunk_list, chunk)

    if first_word is not None and first_word in QUESTION_TYPES.__dict__.values():
        if first_word == QUESTION_TYPES.HOW:
            sec_word = chunk[1] if len(chunk) > 1 else None
            # TODO: how long, how far
            if sec_word is not None and is_adj(sec_word):  # sec_word.dep_ == "amod"???
                return QUESTION_TYPES.COUNT
        return QUESTION_TYPES.__dict__[first_word.upper()]

    return None


# TODO: ilie.doroabt: add the documentation
def _get_first_word(chunk_list: [Span], chunk: Span):
    if is_empty_list(chunk_list) or not isinstance(chunk, Span):
        return None

    if is_preceded_by_conjunction(chunk.root):
        chunk_index = get_chunk_index(chunk_list, chunk)
        # E.g.: "Who is very beautiful and very smart?"
        if chunk_index == -1 or is_verb(chunk.sent[chunk_index]):
            return None
        return _get_first_word(chunk_list, chunk_list[chunk_index - 1])

    return chunk[0].lower_
