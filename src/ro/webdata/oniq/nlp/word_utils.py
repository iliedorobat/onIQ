from spacy.tokens import Span, Token
from ro.webdata.oniq.model.sentence.Action import Action


def get_preposition(sentence: Span, word: Token):
    """
    Extract the preposition of a word

    :param sentence: The target sentence
    :param word: The target token
    :return: The preposition
    """

    last_index = word.i

    for i in reversed(range(0, last_index)):
        crr_word = sentence[i]
        if is_preposition(crr_word):
            return crr_word
        elif is_verb(crr_word):
            return None

    return None


def get_word_before_prep(sentence: Span, word: Token):
    """
    Extract the token before the preposition of a word

    :param sentence: The target sentence
    :param word: The target token
    :return: The token before the preposition of a word
    """

    prep = get_preposition(sentence, word)
    if prep.i == 0:
        return None
    return sentence[prep.i - 1]


def is_conjunction(word: Token):
    """
    Determine if the input word has the role of conjunction or not
    ("and"; "or"; ",").

    :param word: The target token
    :return: True/False
    """

    if word.pos_ == "CCONJ":
        return True
    elif word.pos_ == "PUNCT" and word.text == ",":
        return True
    return False


def is_part_of_action(word: Token, action_list: [Action]):
    """
    Determine if the input word is part of an entry in the action_list

    :param word: The target token
    :param action_list: The list of events (Actions)
    :return: True/False
    """

    for action in action_list:
        for token in action.verb.to_list():
            if token.text == word.text:
                return True

    return False


def is_preposition(word: Token):
    """
    Determine if the input word is a preposition or not

    :param word: The target token
    :return: True/False
    """

    # old: and word.dep_ in ["conj", "prep"]
    return word.pos_ == "ADP" and word.tag_ == "IN"


def is_verb(word: Token):
    """
    Determine if the input word is a verb or not

    :param word:
    :return:
    """

    return word.pos_ in ["AUX", "VERB"]


def is_wh_word(word: Token):
    """
    Check if the token is one of the WH-words\n
    - when, where, why\n
    - whence, whereby, wherein, whereupon\n
    - how\n
    - what, which, whose\n
    - who, whose, which, what\n

    Resources:\n
    - https://grammar.collinsdictionary.com/easy-learning/wh-words\n
    - https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param word: The target token
    :return: True/False
    """

    return word.tag_ in ['WDT', 'WP', 'WP$', 'WRB']
