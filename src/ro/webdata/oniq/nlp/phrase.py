import warnings
from typing import Union
from spacy.tokens import Doc, Span, Token

from ro.webdata.oniq.common.constants import SYSTEM_MESSAGES
from ro.webdata.oniq.model.sentence.Phrase import Phrase
from ro.webdata.oniq.nlp.nlp_utils import get_chunk, get_next_token, get_wh_words
from ro.webdata.oniq.nlp.verb import is_enclosed_by_verb
from ro.webdata.oniq.nlp.word_utils import is_conjunction, is_preposition, is_wh_word


def get_noun_chunks(sentence: Union[Doc, Span]):
    """
    Get the list of noun chunks

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"

    :param sentence: The target sentence
    :return: The list of chunks
    """

    chunk_list = list(sentence.noun_chunks)
    first_chunk = sentence[0:1] if len(sentence) > 0 else None
    first_word = first_chunk[0] if len(first_chunk) > 0 else None

    # include the "which" chunk to the noun chunks list
    # E.g.: "Which is the noisiest and the largest city?"
    if is_nsubj_wh_word(sentence, first_word):
        chunk_list = [first_chunk] + chunk_list
    # E.g.: "Which beautiful female is married to a writer born in Rome and has three children?"
    elif is_wh_word(first_word):
        first_chunk = chunk_list[0]
        last_word = first_chunk[len(first_chunk) - 1]
        chunk_list[0] = sentence[0: last_word.i + 1]

    last_adj_chunk = _get_last_adj_chunk(sentence, chunk_list)

    # FIXME: include the last adjective chunk ???
    # if last_adj_chunk is not None:
    #     chunk_list.append(last_adj_chunk)

    filtered_list = _filter_chunk_list(sentence, chunk_list)

    return _consolidate_noun_chunks(sentence, filtered_list)


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

    for index, chunk in enumerate(chunk_list):
        if len(chunk) == 1:
            if index == 0 or chunk[0] not in get_wh_words(sentence):
                filtered_list.append(chunk)
        else:
            filtered_list.append(chunk)

    return filtered_list


def _get_last_adj_chunk(sentence: Union[Doc, Span], chunk_list: [Span]):
    """
    Get the last chunk that is composed only of the adjective

    E.g.: "Which paintings, large swords or statues do not have more than three owners and are not black?"
        - chunk list: "Which paintings", "large swords", "statues", "more than three owners"
        - adj chunk: "black"

    :param sentence: The target sentence
    :param chunk_list: The list of chunks
    :return: The last chunk that is composed only of the adjective
    """

    last_chunk = chunk_list[len(chunk_list) - 1] if len(chunk_list) > 0 else None
    last_chunk_word = last_chunk[len(last_chunk) - 1] if last_chunk is not None else None
    next_word = sentence[last_chunk_word.i + 1] if last_chunk_word is not None else None

    if next_word is not None and next_word.pos_ != "PUNCT":
        next_word = get_next_token(sentence, next_word, ["AUX", "CCONJ", "PART", "PUNCT", "VERB"])
        return sentence[next_word.i: len(sentence) - 1]

    return None


def get_nouns(phrases: [Phrase]):
    warnings.warn(SYSTEM_MESSAGES.METHOD_IS_OBSOLETE, DeprecationWarning)

    noun_list = []

    for phrase in phrases:
        for token in phrase.content:
            if token.lower_ in ["when", "where", "who", "whose"]:
                # E.g.: 'where are the coins and swords located?'
                # E.g.: 'whose picture is it?'
                noun_list.append(token)
                break
            elif token.pos_ in ["NOUN", "PROPN"] or is_nsubj_wh_word(phrase.content, token):
                noun_list.append(token)

    return noun_list


# 'Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?'
# => 'what is the name of the largest museum which hosts more than 10 pictures and exposed one sword?'
def _consolidate_noun_chunks(sentence: Union[Doc, Span], chunk_list):
    consolidated_list = [chunk_list[0]] \
        if len(chunk_list) > 0 \
        else []

    for index in range(1, len(chunk_list)):
        chunk = chunk_list[index]
        prev_word = sentence[chunk[0].i - 1]

        if is_preposition(prev_word) is True:
            prev_word = sentence[prev_word.i - 1]

            # 1. check if the previous word has the role of conjunction or not
                # E.g.: "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?"
                # E.g.: "What museums are in Bacau, in Iasi or in Bucharest?"
            # 2. check if the previous word is a verb or not
            # E.g.: "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?" [2]
            # chunk_list = ["Which female actor", "Casablanca", "a writer", "Rome", "three children"]
            if not is_conjunction(prev_word) and not is_enclosed_by_verb(prev_word):
                # E.g.: "What is the name of the largest museum?"
                #   - chunks: "what", "the name", "the largest museum"
                #   - consolidated: "what", "the name of the largest museum"
                prev_chunk = consolidated_list[len(consolidated_list) - 1]
                start_index = prev_chunk[0].i
                end_index = chunk[len(chunk) - 1].i + 1
                consolidated_list[len(consolidated_list) - 1] = sentence[start_index: end_index]
            else:
                consolidated_list.append(chunk)
        else:
            consolidated_list.append(chunk)

    return consolidated_list


def get_related_phrase(sentence: Span, phrase_list: [Phrase], phrase_index: int = 0, action_index: int = 0, increment: int = 1):
    """
    Get the phrase which is the object of the current iterated action

    E.g.:
        - question: "Which painting, swords or statues do not have more than three owners?"
        - chunks: "Which painting", "swords", "statues", "more than three owners"
            * "Which painting" [ACTION] "more than three owners"
            * "swords" [ACTION] "more than three owners"
            * "statues" [ACTION] "more than three owners"

    :param sentence: The target sentence
    :param phrase_list: The list of phrases
    :param phrase_index: The index of the current iterated phrase
    :param action_index: The index of the current iterated action
    :param increment: The increment value. If the next phrase is in the relation of conjunction
                      with the current one, go further
    :return: The phrase which is the object of the current iterated action
    """

    index = phrase_index + action_index + increment
    if index >= len(phrase_list):
        return None

    next_phrase = phrase_list[index]
    if next_phrase.chunk.root.dep_ == "conj":
        # E.g.: "Which painting, swords or statues do not have more than three owners?"
        return get_related_phrase(sentence, phrase_list, phrase_index, action_index, increment + 1)
    else:
        return phrase_list[index]


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


def is_nsubj_wh_word(sentence: Span, word: Token):
    """
    Check if the current iterated chunk is composed by only a WH-word in relation of "nsubj"

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"
            * the chunk "Which" is WH-word in relation of "nsubj"

    :param sentence: The target sentence
    :param word: The target token
    :return: True/False
    """

    is_pron_chunk = word.pos_ == "PRON" and word.tag_ == "WP"
    # old: is_preceded_by_aux = sentence[first_word.i + 1].pos_ == "AUX"
    is_preceded_by_aux = sentence[word.i + 1].pos_ == "AUX"

    return is_wh_word(word) and is_preceded_by_aux and not is_pron_chunk


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


def prepare_phrase_list(sentence: Union[Doc, Span]):
    """
    Generate the list of phrases

    :param sentence: The target sentence
    :return: The list of phrases
    """

    phrase_list = _init_phrase_list(sentence)
    _prepare_meta_conj(phrase_list)

    return phrase_list


def _prepare_meta_conj(phrase_list: [Phrase]):
    """
    Set "meta_token" for the phrase with conjunction ","

    E.g.: "What museums are in Bacau, Iasi or Bucharest?"
        - phrase_list: ["What museums", "in Bacau", "Iasi", "Bucharest"]
        - conjunction:      None           None      ","        "or"
        - prepared conj:    None           None      "or"       "or"

    :param phrase_list: The list of phrases
    :return: None
    """

    token = None
    for index, phrase in reversed(list(enumerate(phrase_list))):
        if phrase.conj.token is not None:
            if phrase.conj.token.pos_ == "CCONJ":
                token = phrase.conj.token
            elif phrase.conj.token.pos_ == "PUNCT" and phrase.conj.text == ",":
                phrase.conj.meta_token = token
        else:
            token = None


def _init_phrase_list(sentence: Union[Doc, Span]):
    """
    Generate the list of phrases by including the preposition for each chunk

    :param sentence: The target sentence
    :return: The list of phrases
    """

    phrase_list = []
    chunk_list = get_noun_chunks(sentence)

    for index, chunk in enumerate(chunk_list):
        phrase = Phrase(sentence, chunk_list, index)
        phrase_list.append(phrase)

    return phrase_list
