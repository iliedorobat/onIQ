from typing import Union
from spacy.tokens import Doc, Span

from ro.webdata.oniq.model.sentence.Phrase import Phrase
from ro.webdata.oniq.nlp.chunk_utils import get_noun_chunks


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
        phrase = Phrase(sentence, chunk, chunk_list)
        phrase_list.append(phrase)

    return phrase_list
