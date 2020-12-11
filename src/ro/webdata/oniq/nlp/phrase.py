from typing import Union
from spacy.tokens import Doc, Span
from ro.webdata.oniq.nlp.nlp_utils import get_preposition, get_wh_words


def get_conj_phrases(sentence: Span, index: int):
    """
    Get the phrases which are in the relation of conjunction to the current phrase (phrase_list[index])

    :param sentence: The target sentence
    :param index: The index of the current phrase
    :return: The list of linked phrases
    """

    phrase_list = get_phrase_list(sentence)
    return [
        phrase for phrase in phrase_list
        if phrase.root.dep_ == "conj" and phrase != phrase_list[index]
    ]


def get_main_noun_chunks(sentence: Union[Doc, Span]):
    """
    Exclude the linked phrases from the list of noun chunks

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"
        - the chunks "the noisiest" and "the largest city" needs to be excluded
        in order to build the following statements:
            * "Which is the noisiest"
            * "Which is the largest city"

    :param sentence: The target sentence
    :return: The filtered noun chunks
    """

    chunk_list = get_noun_chunks(sentence)
    return [
        chunk for index, chunk in enumerate(chunk_list)
        if not is_preceded_by_nsubj_wh_word(sentence, chunk_list, index)
    ]


def get_noun_chunks(sentence: Union[Doc, Span]):
    """
    Get the list of noun chunks

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"

    :param sentence: The target sentence
    :return: The list of chunks
    """

    chunk_list = []
    first_chunk = sentence[0:1]

    # include the "which" chunk to the noun chunks list
    if is_nsubj_wh_word(sentence, [first_chunk], 0):
        chunk_list.append(first_chunk)

    chunk_list = chunk_list + list(sentence.noun_chunks)

    return chunk_list


def get_related_phrase(sentence: Span, chunk_index: int = 0, action_index: int = 0, increment: int = 1):
    """
    Get he phrase which is the object of the current iterated action

    E.g.:
        - question: "Which painting, swords or statues do not have more than three owners?"
        - chunks: "Which painting", "swords", "statues", "more than three owners"
            * "Which painting" [ACTION] "more than three owners"
            * "swords" [ACTION] "more than three owners"
            * "statues" [ACTION] "more than three owners"

    :param sentence: The target sentence
    :param chunk_index: The index of the current iterated chunk
    :param action_index: The index of the current iterated action
    :param increment: The increment value. If the next chunk is in the relation of conjunction
                      with the current one, go further
    :return: The phrase which is the object of the current iterated action
    """

    chunk_list = get_noun_chunks(sentence)
    index = chunk_index + action_index + increment
    if index >= len(chunk_list):
        return None

    next_chunk = chunk_list[index]

    if index >= len(chunk_list):
        return None
    if next_chunk.root.dep_ == "conj":
        # E.g.: "Which painting, swords or statues do not have more than three owners?"
        return get_related_phrase(sentence, chunk_index, action_index, increment + 1)
    else:
        return get_phrase(sentence, next_chunk)


def get_related_wh_phrase(sentence: Span, chunk_index: int = 0, action_index: int = 0, increment: int = 1):
    """
    Get he phrase which is the object of the current iterated action.
    The method is applied when the main chunk (chunk_list[chunk_index]) is composed
    by only a WH-word in relation of "nsubj"

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks: "Which", "the noisiest", "the largest city?"
            * "Which" [ACTION] "the noisiest"
            * "Which" [ACTION] "the largest city?"

    :param sentence: The target sentence
    :param chunk_index: The index of the current iterated chunk
    :param action_index: The index of the current iterated action
    :param increment: The increment value
    :return: The phrase which is the object of the current iterated action
    """

    chunk_list = get_noun_chunks(sentence)
    chunk = chunk_list[chunk_index]
    index = chunk_index + action_index + increment

    if index >= len(chunk_list):
        return None
    if len(chunk) == 1 and chunk[0] in get_wh_words(sentence):
        if index == 1 or chunk_list[index].root.dep_ == "conj":
            return get_phrase(sentence, chunk_list[index])


def _get_token_before_aux(sentence: Span, chunk_list: [Span], index: int):
    """
    Get the token before the previous auxiliary verb

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"
            * chunk "Which" => None
            * chunk "the noisiest" => "Which"
            * chunk "the largest city" => "Which"

    :param sentence: The target sentence
    :param chunk_list: The list of chunks
    :param index: The index of the current iterated chunk
    :return: The previous token
    """

    chunk = chunk_list[index]
    prev_index = chunk[0].i - 1

    if prev_index == -1:
        return None

    for i in reversed(range(0, prev_index + 1)):
        token = sentence[i]
        if token.pos_ == "AUX":
            return sentence[token.i - 1]
        elif token.pos_ == "CCONJ":
            return _get_token_before_aux(sentence, chunk_list, index - 1)

    return None


def is_nsubj_wh_word(sentence: Span, chunk_list: [Span], index: int):
    """
    Check if the current iterated chunk is composed by only a WH-word in relation of "nsubj"

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"
            * the chunk "Which" is WH-word in relation of "nsubj"

    :param sentence: The target sentence
    :param chunk_list: The list of chunks
    :param index: The index of the current iterated chunk
    :return: True/False
    """

    first_word = chunk_list[index][0]
    is_wh_word = first_word in get_wh_words(sentence)
    is_pron_chunk = first_word.pos_ == "PRON" and first_word.tag_ == "WP"
    is_preceded_by_aux = sentence[first_word.i + 1].pos_ == "AUX"

    return is_wh_word and is_preceded_by_aux and not is_pron_chunk


def is_preceded_by_nsubj_wh_word(sentence: Span, chunk_list: [Span], index: int):
    """
    Check if the current iterated chunk is preceded by a WH-word which is in relation of "nsubj"

    E.g.:
        - question: "Which is the noisiest and the largest city?"

    :param sentence: The target sentence
    :param chunk_list: The list of chunks
    :param index: The index of the current iterated chunk
    :return: True/False
    """

    prev_token = _get_token_before_aux(sentence, chunk_list, index)
    return prev_token in get_wh_words(sentence) and sentence[prev_token.i + 1].pos_ == "AUX"


def get_phrase(sentence: Span, chunk: Span):
    """
    Generate the phrase by including the preposition for the target chunk

    :param sentence: The target sentence
    :param chunk: The target chunk
    :return: The generated phrase
    """

    preposition = get_preposition(sentence, chunk)
    first_index = preposition.i if preposition is not None else chunk[0].i
    last_index = chunk[len(chunk) - 1].i + 1
    return sentence[first_index: last_index]


def get_phrase_list(sentence: Union[Doc, Span]):
    """
    Generate the list of phrases by including the preposition for each chunk

    :param sentence: The target sentence
    :return: The list of phrases
    """

    chunk_list = get_noun_chunks(sentence)
    return [get_phrase(sentence, chunk) for chunk in chunk_list]
