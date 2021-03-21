from typing import Union
from spacy.tokens import Doc, Span, Token
from ro.webdata.oniq.model.sentence.Phrase import Phrase
from ro.webdata.oniq.nlp.actions import get_action_list
from ro.webdata.oniq.nlp.nlp_utils import get_next_token, get_wh_words
from ro.webdata.oniq.nlp.word_utils import is_conjunction, is_preposition, is_verb


def get_related_phrases(sentence: Span, phrase_list: [Phrase], index: int, action_index: int):
    """
    Get the list of phrases after the event (Action) and which are
    linked to the current phrase

    E.g.:
        - question: "What museums are in Bacau or Bucharest?"
        - target phrase: "What museums"
        - related phrases: "in Bacau", "Bucharest"

    :param sentence: The target sentence
    :param phrase_list: The list of phrases
    :param index: The index of the current phrase
    :param action_index: The index of the current iterated action
    :return: The list of phrases that are linked to the current phrase
    """

    related_phrases = []
    first_related_phrase = _get_first_related_phrase(sentence, phrase_list, index, action_index)
    start_index = phrase_list.index(first_related_phrase)

    for i in range(start_index, len(phrase_list)):
        phrase = phrase_list[i]
        # E.g.: "What museums are in Bacau, Iasi or Bucharest?"
        if phrase == phrase_list[start_index] or phrase.conj.token is not None:
            related_phrases.append(phrase)
        else:
            break

    return related_phrases


def _get_first_related_phrase(sentence: Span, phrase_list: [Phrase], phrase_index: int, action_index: int):
    """
    Get the first phrase which is the object of the current iterated action

    :param sentence: The target sentence
    :param phrase_list: The list of phrases
    :param phrase_index: The index of the current iterated phrase
    :param action_index: The index of the current iterated action
    :return: The phrase which is the object of the current iterated action
    """

    phrase = phrase_list[phrase_index]
    if is_nsubj_wh_word(sentence, phrase.content):
        return get_related_wh_phrase(sentence, phrase_index, action_index)
    return get_related_phrase(sentence, phrase_list, phrase_index, action_index)


def get_target_phrases(sentence: Span, phrase_list: [Phrase], index: int):
    """
    Get the list of phrases before the event (Action)

    E.g.:
        - question: "What museums and sites are in Bacau?"
        - target phrases: "What museums", "sites"
        - related phrase: "in Bacau"

    :param sentence: The target sentence
    :param phrase_list: The list of phrases
    :param index: The index of the current phrase
    :return: The list of target phrases
    """

    target_phrases = []
    first_target_phrase = phrase_list[index]
    start_index = phrase_list.index(first_target_phrase)

    for i in range(start_index, len(phrase_list)):
        phrase = phrase_list[i]
        # E.g.: "Which painting, swords or statues do not have more than three owners?"
        if phrase == phrase_list[start_index] or phrase.conj.token is not None:
            target_phrases.append(phrase)
        else:
            break

    return target_phrases


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
    if is_nsubj_wh_word(sentence, first_chunk):
        chunk_list.append(first_chunk)

    chunk_list = chunk_list + list(sentence.noun_chunks)
    last_adj_chunk = get_last_adj_chunk(sentence, chunk_list)

    # include the last adjective chunk
    if last_adj_chunk is not None:
        chunk_list.append(last_adj_chunk)

    return consolidate_noun_chunks(sentence, chunk_list)


def get_last_adj_chunk(sentence: Union[Doc, Span], chunk_list: [Span]):
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
def consolidate_noun_chunks(sentence: Union[Doc, Span], chunk_list):
    consolidated_list = [chunk_list[0]] \
        if len(chunk_list) > 0 \
        else []

    for index in range(1, len(chunk_list)):
        chunk = chunk_list[index]
        prev_word = sentence[chunk[0].i - 1]

        if is_preposition(prev_word) is True:
            prev_word = sentence[prev_word.i - 1]
            action_list = get_action_list(sentence)

            # 1. check if the "consolidated_list" has been populated
            # 2. check if the previous word has the role of conjunction or not
                # E.g.: "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?"
                # E.g.: "What museums are in Bacau, in Iasi or in Bucharest?"
            # 3. check if the previous word is a verb or not
            # E.g.: "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?" [2]
            # chunk_list = ["Which female actor", "Casablanca", "a writer", "Rome", "three children"]
            if len(consolidated_list) > 0 \
                    and not is_conjunction(prev_word) \
                    and not is_verb(prev_word, action_list):
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
            return Phrase(sentence, chunk_list, index)


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


def is_nsubj_wh_word(sentence: Span, chunk: [Span, Token]):
    """
    Check if the current iterated chunk is composed by only a WH-word in relation of "nsubj"

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"
            * the chunk "Which" is WH-word in relation of "nsubj"

    :param sentence: The target sentence
    :param chunk: The target chunk
    :return: True/False
    """

    first_word = chunk if isinstance(chunk, Token) else chunk[0]
    # TODO: is_wh_word(is_wh_word) => word_utils
    is_wh_word = first_word in get_wh_words(sentence)
    is_pron_chunk = first_word.pos_ == "PRON" and first_word.tag_ == "WP"
    # TODO: check the change: sentence[..] => sentence.doc[...]
    # old: is_preceded_by_aux = sentence[first_word.i + 1].pos_ == "AUX"
    is_preceded_by_aux = sentence.doc[first_word.i + 1].pos_ == "AUX"

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
