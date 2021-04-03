import numpy
import warnings

from ro.webdata.oniq.common.constants import SYSTEM_MESSAGES
from ro.webdata.oniq.model.sentence.Noun import Noun
from ro.webdata.oniq.model.sentence.Phrase import Phrase
from ro.webdata.oniq.nlp.word_utils import is_nsubj_wh_word


def get_nouns(phrases: [Phrase]):
    warnings.warn(SYSTEM_MESSAGES.METHOD_IS_OBSOLETE, DeprecationWarning)

    noun_list = []

    for phrase in phrases:
        for token in phrase.content:
            if token.lower_ in ["when", "where", "who", "whose"]:
                # E.g.: "Where are the coins and swords located?"
                # E.g.: "Whose picture is it?"
                noun_list.append(token)
                break
            elif token.pos_ in ["NOUN", "PROPN"] or is_nsubj_wh_word(phrase.content, token):
                noun_list.append(token)

    return noun_list


def get_noun_list(chunk, *dependencies: []):
    """
    Get the list of nouns in a sentence

    :param dependencies: The list of dependencies used for filtering
    :param chunk: The sentence
    :return: The list of nouns
    """

    warnings.warn(SYSTEM_MESSAGES.METHOD_IS_OBSOLETE, DeprecationWarning)

    nouns = []

    for token in chunk:
        if token.tag_[0:2] == "NN" and (
                len(dependencies) == 0 or token.dep_ in numpy.asarray(dependencies)
        ):
            nouns.append(
                Noun(token.dep_, token.text == chunk.root.text, token)
            )

    return nouns
