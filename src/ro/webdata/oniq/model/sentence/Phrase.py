from spacy.tokens import Span, Token

from ro.webdata.oniq.model.sentence.Conjunction import Conjunction
from ro.webdata.oniq.nlp.chunk_utils import extract_chunk, extract_comparison_adv, extract_determiner, \
    get_chunk_index, get_noun_chunks
from ro.webdata.oniq.nlp.utils import is_empty_list
from ro.webdata.oniq.nlp.word_utils import get_next_word, get_preposition, get_prev_word, is_adj, is_conjunction, \
    is_followed_by_conjunction, is_preceded_by_conjunction, is_preposition, is_verb, is_wh_word


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

    def __init__(self, chunk: Span, phrase_type: str):
        self.chunk = chunk
        self.conj = _prepare_conjunction(self.chunk)

        self.comparison_adv = extract_comparison_adv(chunk)
        self.det = extract_determiner(self.chunk)
        self.prep = get_preposition(self.chunk.root)
        self.meta_prep = _prepare_meta_prep(self.chunk, self.prep)

        self.phrase_type = phrase_type
        self.question_type = _prepare_question_type(self.chunk)
        self.text = _prepare_text(self.chunk,  self.comparison_adv, self.det, self.prep, self.meta_prep)
        self.prep_phrase = _prepare_prep_chunk(self.chunk)

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
        return (
            f'{indentation}{phrase_type}: {{\n'
            f'{indentation}\toperator: {self.conj}\n'
            f'{indentation}\tphrase: {self.text}\n'
            f'{indentation}\tprep_phrase: {self.prep_phrase}\n'
            f'{indentation}\ttype: {self.question_type}\n'
            f'{indentation}}}'
        )


def _prepare_conjunction(chunk: Span):
    """
    Prepare the conjunction

    :param chunk: The current iterated chunk
    :return: Conjunction object
    """

    if not isinstance(chunk, Span):
        return None

    sentence = chunk.sent
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


def _prepare_prep_chunk(chunk: Span):
    """
    Extract the span that is linked to the input chunk through a preposition

    E.g.:
        - question: "Who is starring in the film series of Souls of the Departed?"
            - chunks: ["who", "in the film series", "of Souls", "of the Departed"]
                - chunk: "who"                      prep_chunk: None
                - chunk: "in the film series"       prep_chunk: "of Souls of the Departed"
        - question: "Who is the director of Amsterdam museum?"
            - chunks: ["who", "the director", "of Amsterdam museum"]
                - chunk: "who"                      prep_chunk: None
                - chunk: "the director"             prep_chunk: "of Amsterdam museum"

    :param chunk: The target chunk
    :return: The prepared preposition chunk
    """

    if not isinstance(chunk, Span):
        return None

    sentence = chunk.sent
    noun_chunk_list = list(sentence.noun_chunks)

    chunk_index = get_chunk_index(noun_chunk_list, chunk)
    last_word = chunk[len(chunk) - 1]
    next_word = get_next_word(last_word)

    prep_phrase = None
    for index, noun_chunk in enumerate(noun_chunk_list):
        if index > chunk_index:
            # E.g.: "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?"
            if not is_wh_word(next_word) and is_preposition(next_word) and next_word.dep_ == "prep":
                last_word = noun_chunk[len(noun_chunk) - 1]
                next_word = get_next_word(last_word)

                # E.g.: "Who is starring in the film series of Souls of the Departed?" [1]
                # E.g.: "Where does the holder of the position of Lech Kaczynski live?" [1]
                if isinstance(prep_phrase, Span):
                    prep_phrase = sentence[prep_phrase.start: noun_chunk.end]

                # E.g.: "Who is the director of Amsterdam museum?"
                # E.g.: "How many paintings are on display at the Amsterdam Museum?"
                else:
                    prep_phrase = noun_chunk

            # Exit the loop if the next_word is not a preposition
            else:
                break

    return prep_phrase


def _prepare_text(chunk: Span, comparison_adv: Token, det: Token, prep: Token, meta_prep: Token):
    """
    Prepare the text which will be displayed

    :param chunk: The target chunk
    :param prep: The preposition of the phrase
    :param meta_prep: The preposition of the previous related phrase
    :return: The text
    """

    if not isinstance(chunk, Span):
        return None

    question_type = _prepare_question_type(chunk)
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
        # E.g.: "How old are you?" [6]
        if isinstance(question_type, Span) and question_type.text in chunk.text:
            start = chunk.start + len(question_type)
            text = chunk[start: chunk.end].text

    if isinstance(question_type, Span):
        if question_type.text.lower() not in text:
            return f'{question_type} {text}'.strip()

    return f'{text}'


def _prepare_question_type(chunk: Span):
    """
    Extract the type of the question

    :param chunk: The target chunk
    :return: what, why, how, how long, etc.
    """

    if not isinstance(chunk, Span):
        return None

    chunk_list = get_noun_chunks(chunk.sent)
    first_word = _get_first_word(chunk_list, chunk)

    if is_wh_word(first_word):
        if first_word.lower_ == "how":
            how_chunk = extract_chunk(chunk_list, first_word)
            second_word = how_chunk[1] if len(how_chunk) > 1 else None

            # E.g.: "How many paintings are on display at the Amsterdam Museum?"
            if is_adj(second_word):
                return chunk.sent[first_word.i: second_word.i + 1]

        return chunk.sent[first_word.i: first_word.i + 1]

    return None


# TODO: ilie.dorobat: add the documentation
def _get_first_word(chunk_list: [Span], chunk: Span):
    if is_empty_list(chunk_list) or not isinstance(chunk, Span):
        return None

    if is_preceded_by_conjunction(chunk.root):
        chunk_index = get_chunk_index(chunk_list, chunk)
        # E.g.: "Who is very beautiful and very smart?"
        if chunk_index == -1 or is_verb(chunk.sent[chunk_index]):
            return None
        return _get_first_word(chunk_list, chunk_list[chunk_index - 1])

    return chunk[0]
