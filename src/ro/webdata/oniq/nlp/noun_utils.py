import numpy
import warnings

from spacy.tokens import Span, Token

from ro.webdata.oniq.common.constants import SYSTEM_MESSAGES
from ro.webdata.oniq.model.sentence.Noun import Noun
from ro.webdata.oniq.model.sentence.Phrase import Phrase
from ro.webdata.oniq.nlp.word_utils import is_linked_by_conjunction, is_noun, is_nsubj_wh_word, is_wh_adverb


def is_linked_noun(word: Token):
    """
    Determine if the input word is preceded or followed by a conjunction

    :param word: The target word
    :return: True/False
    """

    if not isinstance(word, Token) or not is_noun(word):
        return False

    return is_linked_by_conjunction(word)


def get_noun_ancestor(chunk: Span):
    """
    Extract the first NOUN / PROPN from the list of ancestors

    :param chunk: The current iterated chunk
    :return: The noun ancestor
    """

    if not isinstance(chunk, Span):
        return None

    ancestors = chunk.root.ancestors
    for token in ancestors:
        if is_noun(token):
            return token

    return None


# TODO: check get_nouns and get_noun_list
def get_nouns(phrases: [Phrase]):
    warnings.warn(SYSTEM_MESSAGES.METHOD_IS_OBSOLETE, DeprecationWarning)

    noun_list = []

    if not isinstance(phrases, list):
        return noun_list

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


def get_noun_list(chunk: Span):
    """
    Get the list of nouns in a chunk

    :param chunk: The target chunk
    :return: The list of nouns
    """

    noun_list = []

    if not isinstance(chunk, Span):
        return noun_list

    for token in chunk:
        if token.pos_ in ["NOUN", "PROPN"] \
                or is_nsubj_wh_word(chunk.sent, token) \
                or is_wh_adverb(token):
            noun_list.append(token)

    return noun_list


# def get_noun_list(chunk, *dependencies: []):
#     """
#     Get the list of nouns in a sentence
#
#     :param dependencies: The list of dependencies used for filtering
#     :param chunk: The sentence
#     :return: The list of nouns
#     """
#
#     warnings.warn(SYSTEM_MESSAGES.METHOD_IS_OBSOLETE, DeprecationWarning)
#
#     nouns = []
#
#     for token in chunk:
#         if token.tag_[0:2] == "NN" and (
#                 len(dependencies) == 0 or token.dep_ in numpy.asarray(dependencies)
#         ):
#             nouns.append(
#                 Noun(token.dep_, token.text == chunk.root.text, token)
#             )
#
#     return nouns
