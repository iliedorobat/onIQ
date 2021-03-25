from spacy.tokens import Token
from ro.webdata.oniq.nlp.word_utils import is_verb, is_acomp


def is_enclosed_by_verb(word: Token):
    """
    # TODO: is_part_of?
    Determine if the input word is qualified to be part of a Verb statement

    :param word: The target token
    :return: True/False
    """

    return is_verb(word) or is_acomp(word)
