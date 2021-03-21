from spacy.tokens import Token
from ro.webdata.oniq.model.sentence.Action import Action


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


def is_preposition(word: Token):
    """
    Determine if the input work is a preposition or not

    :param word: The target token
    :return: True/False
    """

    # old: and word.dep_ in ["conj", "prep"]
    return word.pos_ == "ADP" and word.tag_ == "IN"


def is_verb(word: Token, action_list: [Action]):
    """
    Determine if the input word is a verb or not

    :param word: The target token
    :param action_list: The list of events (Actions)
    :return: True/False
    """

    for action in action_list:
        for token in action.verb.to_list():
            if token.text == word.text:
                return True

    return False


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
