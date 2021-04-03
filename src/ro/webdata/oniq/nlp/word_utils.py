from spacy.tokens import Span, Token


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


def is_noun(word: Token):
    """
    Determine if the input word is a noun or not

    :param word: The target token
    :return: True/False
    """

    return word.pos_ in ["NOUN", "PROPN"]


def is_nsubj_wh_word(sentence: Span, word: Token):
    """
    Check if the current word is part of a chunk which is composed by
    only a WH-word in relation of "nsubj"

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"
            * the chunk "Which" is WH-word in relation of "nsubj"

    :param sentence: The target sentence
    :param word: The target token
    :return: True/False
    """

    is_pron_chunk = word.pos_ == "PRON" and word.tag_ == "WP"
    is_preceded_by_aux = sentence[word.i + 1].pos_ == "AUX"

    return is_wh_word(word) and is_preceded_by_aux and not is_pron_chunk


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

    :param word: The target token
    :return: True/False
    """

    return word.pos_ in ["AUX", "VERB"]


def is_acomp(word: Token):
    """
    Determine if the input word is an adjectival complement

    :param word: The target token
    :return: True/False
    """

    return word.pos_ == "ADJ" and word.dep_ == "acomp"


def is_wh_adverb(word: Token):
    """
    Check if the input word is an adverb (tag = 'WRB'):\n
    - when, where, why\n
    - whence, whereby, wherein, whereupon\n
    - how\n

    Resources:\n
    - https://grammar.collinsdictionary.com/easy-learning/wh-words\n
    - https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param word: The target token
    :return: True/False
    """

    return word.tag_ == 'WRB'


def is_wh_word(word: Token):
    """
    Check if the input word is one of the WH-words\n
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
