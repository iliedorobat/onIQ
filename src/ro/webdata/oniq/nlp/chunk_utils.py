import warnings
from typing import Union
from spacy.tokens import Doc, Span, Token

from ro.webdata.oniq.common.constants import SYSTEM_MESSAGES
from ro.webdata.oniq.nlp.adv_utils import get_comparison_adv
from ro.webdata.oniq.nlp.nlp_utils import get_wh_words
from ro.webdata.oniq.nlp.utils import is_doc_or_span, is_empty_list
from ro.webdata.oniq.nlp.word_utils import get_next_word, get_prev_word, is_adj, is_adv, is_aux_verb, is_cardinal, \
    is_common_det, is_linked_by_conjunction, is_noun, is_preposition, is_verb, is_wh_det, is_wh_word


def extract_chunk(chunk_list: [Span], word: Token):
    """
    Retrieve the chunk which contains the input token

    :param word: The token to be searched for
    :param chunk_list: The list of chunks (use case: "noun_chunks")
    :return: The identified chunk which contains the input token
    """

    if is_empty_list(chunk_list) or not isinstance(word, Token):
        return None

    # E.g.: "Where was the last place the picture was exposed?"
    if word.i == 0:
        return chunk_list[0]

    for chunk in chunk_list:
        for token in chunk:
            if word == token:
                return chunk

    return None


def extract_comparison_adv(chunk: Span):
    """
    Get the superlative/comparative adverb that precedes the chunk

    E.g.: "Which is the noisiest, the most beautiful and the largest city?"

    :param chunk: The target chunk
    :return: The superlative/comparative adverb that precedes the chunk
    """

    if not isinstance(chunk, Span):
        return None

    return get_comparison_adv(chunk[0])


def extract_determiner(chunk: Span):
    """
    Get the determiner placed before a noun chunk

    :param chunk: The target noun chunk
    :return: The determiner
    """

    if not isinstance(chunk, Span):
        return None

    prev_word = get_prev_word(chunk[0])
    while is_adv(prev_word):
        prev_word = get_prev_word(prev_word)

    if not is_common_det(prev_word):
        return None

    return prev_word


def get_first_word(chunk: Span):
    """
    Get the first word from a chunk

    :param chunk: The target noun chunk
    :return: The determiner
    """

    if not isinstance(chunk, Span) or len(chunk) == 0:
        return None

    return chunk[0]


def get_chunk_index(chunk_list: [Span], chunk: Span):
    """
    Retrieve the chunk's position in chunk_list

    :param chunk_list: The list of chunks (use case: "noun_chunks")
    :param chunk: The target chunk
    :return: The index of the target chunk
    """

    if not isinstance(chunk, Span) or is_empty_list(chunk_list):
        return -1

    for index, crr_chunk in enumerate(chunk_list):
        if crr_chunk == chunk:
            return index

    return -1


def get_prev_chunk(chunk_list: [Span], chunk: Span):
    warnings.warn(SYSTEM_MESSAGES.METHOD_NOT_USED, DeprecationWarning)

    if not isinstance(chunk, Span) or is_empty_list(chunk_list):
        return None

    chunk_index = chunk_list.index(chunk)
    if chunk_index > 0:
        return chunk_list[chunk_index - 1]

    return None


def is_linked_chunk(chunk: Span):
    """
    Determine if the input chunk is preceded or followed by a conjunction

    :param chunk: The target chunk
    :return: True/False
    """

    if not isinstance(chunk, Span):
        return False

    return is_linked_by_conjunction(chunk[0])


def get_noun_chunks(sentence: Union[Doc, Span]):
    """
    Get the list of noun chunks

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"

    :param sentence: The target sentence
    :return: The list of chunks
    """

    if not is_doc_or_span(sentence):
        return []

    chunk_list = _get_extended_noun_chunks(sentence)
    wh_span = _get_wh_span(sentence)
    first_word = get_first_word(wh_span)

    # include the "which/how" chunk to the noun chunks list
    # TODO: move to _get_extended_noun_chunks
    if is_wh_word(first_word):
        next_word = get_next_word(wh_span[len(wh_span) - 1])

        if is_verb(next_word):
            # E.g.: "How long does the museum remain closed?"
            if first_word.lower_ == "how" and next_word.dep_ != "ROOT":
                first_chunk = chunk_list[0]
                last_word = first_chunk[len(first_chunk) - 1]
                chunk_list[0] = sentence[0: last_word.i + 1]

            # E.g.: "How long is the journey?"
            # E.g.: "When was anıtkabir built?" [3]
            else:
                chunk_list = [wh_span] + chunk_list

    # TODO: remove (see _get_extended_noun_chunks)
    # E.g.: "What did James Cagney win in the 15th Academy Awards?" [1]
    if is_wh_word(chunk_list[0][0]) and len(chunk_list) > 1:
        first_word = chunk_list[0][0]
        second_chunk = chunk_list[1]
        if first_word in second_chunk:
            chunk_list.remove(chunk_list[0])

    return _filter_chunk_list(sentence, chunk_list)


# TODO: ilie.dorobat: check the utility of _filter_chunk_list
def _filter_chunk_list(sentence: Union[Doc, Span], chunk_list: [Span]):
    """
    Exclude the WH-words chunks-like from the list of chunks, excepting for the first entry

    E.g.: "Who is the director who own 2 cars and sold a house or a panel?"
        - chunk_list = ["Who", "the director", "who", "10 cars", "a house", "a panel"]
        - WH-words chunks-like: [chunk_list[2]]
        - filtered_list = ["Who", "the director", "10 cars", "a house", "a panel"]

    :param sentence: The target sentence
    :param chunk_list: The target list of chunks
    :return: The filtered list of chunks
    """

    filtered_list = []

    if not is_doc_or_span(sentence) or is_empty_list(chunk_list):
        return filtered_list

    for index, chunk in enumerate(chunk_list):
        if len(chunk) == 1:
            if index == 0 or chunk[0] not in get_wh_words(sentence):
                filtered_list.append(chunk)
        else:
            filtered_list.append(chunk)

    return filtered_list


# TODO: ilie.dorobat: documentation
def _get_extended_noun_chunks(sentence: Union[Doc, Span]):
    # FIXME
    # E.g.: "The Goddess of Democracy, also known as the Goddess of Democracy and Freedom, the Spirit of Democracy,
    # and the Goddess of Liberty (自由女神; zìyóu nǚshén), was a 10-metre-tall (33 ft) statue created during the day
    # of April 10 Tiananmen Square protests"

    chunk_list = []

    if not is_doc_or_span(sentence):
        return chunk_list

    initial_chunks = _get_merged_prep_chunks(sentence)
    for index, initial_chunk in enumerate(initial_chunks):
        chunk_list.append(
            _prepare_chunk(initial_chunk)
        )

    # TODO: documentation
    # E.g.: "What did James Cagney win in the 15th Academy Awards?" [1]
    if is_wh_word(chunk_list[0][0]) and len(chunk_list) > 1:
        first_word = chunk_list[0][0]
        second_chunk = chunk_list[1]
        if first_word in second_chunk:
            chunk_list.remove(chunk_list[0])

    return chunk_list


def _get_wh_span(sentence: Union[Doc, Span]):
    """
    Retrieve the tokens that form the starting wh-span ("which", "what", "how", "how long", etc.)

    :param sentence: The target sentence
    :return: The wh-span
    """

    if not is_doc_or_span(sentence):
        return None

    first_word = get_first_word(sentence)
    if is_wh_word(first_word):
        # E.g.: "How far is Pattaya from Bangkok?" [1]
        # E.g.: "How old are you?" [6]
        if first_word.lower_ == "how":
            if is_adj(sentence[1]) or is_adv(sentence[1]):
                return sentence[0:2]

        # E.g.: "When was anıtkabir built?" [3]
        return sentence[0:1]

    return None


def _get_merged_prep_chunks(sentence: Union[Doc, Span]):
    """
    Merge te chunks that are linked through a preposition and get the prepared list

    E.g.:
        - question: "Who is the director of Amsterdam museum?"
        - chunks: ["who", "the director", "Amsterdam museum"]
        - merged chunks: ["who", "the director of Amsterdam museum"]

    :param sentence: The target sentence
    :return: The list of prepared chunks
    """

    if not is_doc_or_span(sentence):
        return None

    chunk_list = []
    noun_chunk_list = list(sentence.noun_chunks)

    for index, chunk in enumerate(noun_chunk_list):
        if index == 0:
            chunk_list.append(chunk)
        if index == len(noun_chunk_list) - 1:
            break

        last_word = chunk[len(chunk) - 1]
        next_word = get_next_word(last_word)
        next_chunk = noun_chunk_list[index + 1]

        # Merge two chunks that are linked through a preposition
        # E.g.: "Who is the director of Amsterdam museum?"
        # E.g.: "How many paintings are on display at the Amsterdam Museum?"
        # E.g.: "Where does the holder of the position of Lech Kaczynski live?" [1]
        if is_preposition(next_word) and next_word.dep_ == "prep":
            crr_chunk = chunk_list[len(chunk_list) - 1]
            chunk_list[len(chunk_list) - 1] = sentence[crr_chunk.start: next_chunk.end]
        else:
            chunk_list.append(next_chunk)

    return chunk_list


# TODO: ilie.dorobat: documentation
def _prepare_chunk(chunk: Span):
    chunk_list = list(chunk.sent.noun_chunks)
    prev_word = get_prev_word(chunk[0])
    aux_verb = None

    # E.g.: "What did James Cagney win in the 15th Academy Awards?" [1]
    if is_aux_verb(prev_word):
        aux_verb = prev_word
        prev_word = get_prev_word(prev_word)

    # E.g.: "Which one of the most beautiful paintings has not been moved to Bacau?"
    while is_preposition(prev_word) or is_cardinal(prev_word):
        prev_word = get_prev_word(prev_word)

    # E.g.: "How many beautiful days do I have to wait until the opening?"
    while (is_noun(prev_word) and prev_word.dep_ == "npadvmod") or is_adj(prev_word):
        prev_word = get_prev_word(prev_word)

    if is_wh_word(prev_word):
        # TODO: ilie.dorobat: simplify by checking if verb.dep_ == "aux"?
        if (prev_word.lower_ == "what" and prev_word.dep_ in ["dobj", "pobj"]) or \
                (prev_word.lower_ == "which" and is_wh_det(prev_word)) or \
                (prev_word.lower_ == "how" and aux_verb is not None and aux_verb.dep_ == "aux"):
            # E.g.: "When was anıtkabir built?" [3]
            prev_chunk = chunk.sent[prev_word.i: prev_word.i + 1]
            prev_chunk_index = get_chunk_index(chunk_list, prev_chunk)

            # Return a custom chunk only if prev_word is not already part of a chunk
            if prev_chunk_index == -1:
                return chunk.sent[prev_word.i: chunk.end]

    return chunk
