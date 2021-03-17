from typing import Union
from spacy.tokens import Doc, Span, Token
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Phrase import Phrase
from ro.webdata.oniq.nlp.actions import get_action_list
from ro.webdata.oniq.nlp.nlp_utils import get_next_token, get_wh_words


def get_related_phrases(sentence: Span, index: int, action: Action):
    """
    Get the list of phrases after the event (Action) and which are
    linked to the current phrase

    E.g.:
        - question: "What museums are in Bacau or Bucharest?"
        - target phrase: "What museums"
        - related phrases: "in Bacau", "Bucharest"

    :param sentence: The target sentence
    :param index: The index of the current phrase
    :param action: The event of the current phrase
    :return: The list of phrases that are linked to the current phrase
    """

    conj_phrases = get_conj_phrases(sentence, index)

    aux_verb = action.verb.aux_vbs[0] \
        if action.verb.aux_vbs is not None \
        else None
    verb = action.verb.main_vb \
        if action.verb.main_vb is not None \
        else aux_verb

    return list(
        filter(
            lambda item: verb.i < item.content[0].i, conj_phrases
        )
    )


def get_target_phrases(sentence: Span, phrase_list: [Phrase], index: int, action: Action):
    """
    Get the list of phrases before the event (Action)

    E.g.:
        - question: "What museums and sites are in Bacau?"
        - target phrases: "What museums", "sites"
        - related phrase: "in Bacau"

    :param sentence: The target sentence
    :param phrase_list: The list of phrases
    :param index: The index of the current phrase
    :param action: The event of the current phrase
    :return: The list of target phrases
    """

    main_target_phrase = phrase_list[index]
    conj_phrases = get_conj_phrases(sentence, index)

    def is_last_phrase():
        for conj_phrase in conj_phrases:
            if conj_phrase.i > main_target_phrase.i:
                return False
        return True

    target_phrases = [main_target_phrase] + conj_phrases
    if is_last_phrase() is True:
        target_phrases = conj_phrases + [main_target_phrase]

    aux_verb = action.verb.aux_vbs[0] \
        if action.verb.aux_vbs is not None \
        else None
    verb = action.verb.main_vb \
        if action.verb.main_vb is not None \
        else aux_verb

    return list(
        filter(
            lambda item: verb.i > item.content[0].i, target_phrases
        )
    )


def get_conj_phrases(sentence: Span, index: int):
    """
    Get the phrases which are in the relation of conjunction to the current phrase (phrase_list[index])

    :param sentence: The target sentence
    :param index: The index of the current phrase
    :return: The list of linked phrases
    """

    phrase_list = get_phrase_list(sentence, False)
    return [
        phrase for phrase in phrase_list
        if phrase.content.root.dep_ == "conj" and phrase != phrase_list[index]
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
    consolidated_list = []

    for index, chunk in enumerate(chunk_list):
        prev_word = sentence[chunk[0].i - 1]

        # E.g.: 'what is the name of the largest museum?'
        #   - chunks: "what", "the name", "the largest museum"
        #   - consolidated: "what", "the name of the largest museum"
        if prev_word.pos_ == "ADP" and prev_word.dep_ == "prep":
            prev_word = sentence[prev_word.i - 1]
            if len(consolidated_list) > 0 and not checking(sentence, prev_word):
                prev_chunk = consolidated_list[len(consolidated_list) - 1]
                start_index = prev_chunk[0].i
                end_index = chunk[len(chunk) - 1].i + 1
                consolidated_list[len(consolidated_list) - 1] = sentence[start_index: end_index]
            else:
                consolidated_list.append(chunk)
        else:
            consolidated_list.append(chunk)

    return consolidated_list


def checking(sentence: Union[Doc, Span], word: Token):
    action_list = get_action_list(sentence)

    for action in action_list:
        for token in action.verb.to_list():
            if token.text == word.text:
                return True

    return False


def get_related_phrase(sentence: Span, phrase_index: int = 0, action_index: int = 0, increment: int = 1):
    """
    Get the phrase which is the object of the current iterated action

    E.g.:
        - question: "Which painting, swords or statues do not have more than three owners?"
        - chunks: "Which painting", "swords", "statues", "more than three owners"
            * "Which painting" [ACTION] "more than three owners"
            * "swords" [ACTION] "more than three owners"
            * "statues" [ACTION] "more than three owners"

    :param sentence: The target sentence
    :param phrase_index: The index of the current iterated phrase
    :param action_index: The index of the current iterated action
    :param increment: The increment value. If the next phrase is in the relation of conjunction
                      with the current one, go further
    :return: The phrase which is the object of the current iterated action
    """

    chunk_list = get_noun_chunks(sentence)
    index = phrase_index + action_index + increment
    if index >= len(chunk_list):
        return None

    next_chunk = chunk_list[index]

    if index >= len(chunk_list):
        return None
    if next_chunk.root.dep_ == "conj":
        # E.g.: "Which painting, swords or statues do not have more than three owners?"
        return get_related_phrase(sentence, phrase_index, action_index, increment + 1)
    else:
        return Phrase(sentence, next_chunk, False)


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
            return Phrase(sentence, chunk_list[index], False)


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


def get_phrase_list(sentence: Union[Doc, Span], is_target: bool = False):
    """
    Generate the list of phrases by including the preposition for each chunk

    :param sentence: The target sentence
    :param is_target: Specify whether or not a is target phrase
    :return: The list of phrases
    """

    chunk_list = get_noun_chunks(sentence)
    return [
        Phrase(sentence, chunk, is_target)
        for chunk in chunk_list
    ]
