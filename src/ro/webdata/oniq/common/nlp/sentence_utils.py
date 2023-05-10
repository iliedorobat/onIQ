from spacy.tokens import Span

from ro.webdata.oniq.common.nlp.word_utils import is_wh_word, is_verb


def get_root(sentence: Span):
    """
    Lookup for the main head (root) of the sentence.

    :param sentence: The target sentence.
    :return: A Token representing the main head of the sentence.
    """

    if not isinstance(sentence, Span):
        return None

    return sentence.root


def contains_multiple_wh_words(sentence: Span):
    """
    Determine if the sentence contains two or more WH-words.

    E.g.:
        - question: "Where was the person born whose successor was Le Hong Phong?"

    :param sentence: The target sentence.
    :return: True/False
    """

    if not isinstance(sentence, Span):
        return None

    counter = 0

    for token in sentence:
        if is_wh_word(token):
            counter += 1

    return counter > 1


def ends_with_verb(sentence: Span):
    """
    Determine if the sentence ends with a verb.

    :param sentence: The target sentence.
    :return: True/False
    """

    if not isinstance(sentence, Span):
        return None

    tokens = [token for token in sentence if token.pos_ != "PUNCT"]
    last_token = tokens[len(tokens) - 1]

    return is_verb(last_token)
