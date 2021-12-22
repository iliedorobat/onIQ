from spacy.tokens import Span, Token
import warnings


def get_preposition(word: Token):
    """
    Extract the preposition of a word

    :param word: The target token
    :return: The preposition that precedes the token
    """

    if not isinstance(word, Token):
        return None

    for index, token in list(reversed(list(enumerate(word.sent)))):
        if index < word.i:
            if is_preposition(token):
                return token
            elif is_verb(token):
                return None

    return None


# TODO: ilie.dorobat: to be used in other places as well (next_word)
def get_next_word(word: Token):
    """
    Get the token after the input word

    :param word: The target word
    :return: The token after the input word
    """

    if not isinstance(word, Token):
        return None

    next_index = word.i + 1

    if next_index == len(word.sent):
        return None

    return word.sent[next_index]


# TODO: ilie.dorobat: to be used in other places as well (prev_word)
def get_prev_word(word: Token):
    """
    Get the token before the input word

    :param word: The target word
    :return: The token before the input word
    """

    if not isinstance(word, Token):
        return None

    prev_index = word.i - 1

    if prev_index < 0:
        return None

    return word.sent[prev_index]


def is_cardinal(word: Token):
    """
    Determine if the input word is a cardinal number

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ == "NUM" and word.tag_ == "CD"


def is_conjunction(word: Token):
    """
    Determine if the input word has the role of conjunction or not
    ("and"; "or"; ",").

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

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

    if not isinstance(word, Token):
        return False

    return word.pos_ in ["NOUN", "PROPN"]


def is_linked_by_conjunction(word: Token):
    """
    Determine if the input word is preceded or followed by a conjunction

    :param word: The target word
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    if is_conjunction(word):
        return True

    prev_word = get_prev_word(word)
    next_word = get_next_word(word)

    return is_preceded_by_conjunction(prev_word) or is_followed_by_conjunction(next_word)


def is_preceded_by_conjunction(word: Token):
    """
    Determine if the input word is preceded by a conjunction

    :param word: The target word
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    # 1. if the iterator has reached to the beginning of the phrase
    # 2. if the iterator will reach to the previous phrase
    if is_verb(word):
        return False

    if is_conjunction(word):
        return True

    prev_word = get_prev_word(word)
    return is_preceded_by_conjunction(prev_word)


def is_followed_by_conjunction(word: Token):
    """
    Determine if the input word is followed by a conjunction

    :param word: The target word
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    # 1. if the iterator has reached to the end of the phrase
    # 2. if the iterator has reached the next phrase
    if is_verb(word):
        return False

    if is_conjunction(word):
        return True

    next_word = get_next_word(word)
    return is_followed_by_conjunction(next_word)


def is_followed_by_preposition(word: Token):
    """
    Determine if the input word is followed by a preposition

    E.g.:
        - question: "Where does the holder of the position of Lech Kaczynski live?" [1]
        - question: "What is the population and area of the most populated state?" [2]

    :param word: The target word
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    # 1. if the iterator has reached to the end of the phrase
    # 2. if the iterator has reached the next phrase
    # is_conjunction(word) => E.g.: "What is the population and area of the most populated state?" [2]
    if is_verb(word) or is_conjunction(word):
        return False

    if is_preposition(word):
        return True

    next_word = get_next_word(word)
    return is_followed_by_preposition(next_word)


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

    if not isinstance(word, Token) or not isinstance(sentence, Span):
        return False

    warnings.warn("deprecated in favour of is_wh_noun_chunk", DeprecationWarning)

    is_pron_chunk = word.pos_ == "PRON" and word.tag_ == "WP"
    is_followed_by_aux = sentence[word.i + 1].pos_ == "AUX"

    return is_wh_word(word) and is_followed_by_aux and not is_pron_chunk


def is_preposition(word: Token):
    """
    Determine if the input word is a preposition or not

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ == "ADP" and word.tag_ == "IN"


def is_verb(word: Token):
    """
    Determine if the input word is a verb or not

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ in ["AUX", "VERB"]


def is_aux_verb(word: Token):
    """
    Determine if the input word is an auxiliary verb or not

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ == "AUX"


def is_adj(word: Token):
    """
    Determine if the input word is an adjective

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ == "ADJ"


def is_adj_comparative(word: Token):
    """
    Determine if the input word is a comparative adjective

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return is_adj(word) and word.tag_ == "JJR"


def is_adj_complement(word: Token):
    """
    Determine if the input word is an adjectival complement

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return is_adj(word) and word.dep_ == "acomp"


def is_adj_modifier(word: Token):
    """
    Determine if the input word is an adjectival modifier

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return is_adj(word) and word.dep_ == "amod"


def is_adv(word: Token):
    """
    Determine if the input word is an adverb

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ == "ADV"


def is_common_det(word: Token):
    """
    Determine if the input word is a common determiner ("a", "the")

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ == "DET" \
        and word.tag_ == "DT" \
        and word.dep_ == "det"


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

    if not isinstance(word, Token):
        return False

    return word.tag_ == 'WRB'


def is_wh_det(word: Token):
    """
    Determine if the input word is wh-determiner ("which", etc.)

    :param word: The target token
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ == "DET" \
           and word.tag_ == "WDT" \
           and word.dep_ == "det"


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

    if not isinstance(word, Token):
        return False

    return word.tag_ in ['WDT', 'WP', 'WP$', 'WRB']
