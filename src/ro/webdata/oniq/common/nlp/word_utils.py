import warnings

from spacy.tokens import Span, Token

AUXILIARY_VERBS = [
    # common auxiliary verbs
    "be",
    "do",
    "have",
    # modal auxiliary verbs
    "can",
    "could",
    "may",
    "might",
    "must",
    "ought to",
    "shall",
    "should",
    "will",
    "would"
]


def get_preposition(word: Token):
    """
    Extract the preposition of the input word.

    :param word: The target token.
    :return: The preposition that precedes the token.
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


def get_next_word(word: Token):
    """
    Get the token after the input word.

    :param word: The target word.
    :return: The token after the input word.
    """

    if not isinstance(word, Token):
        return None

    next_index = word.i + 1

    if next_index == len(word.sent):
        return None

    return word.sent[next_index]


def get_prev_word(word: Token):
    """
    Get the token before the input word.

    :param word: The target word.
    :return: The token before the input word.
    """

    if not isinstance(word, Token):
        return None

    prev_index = word.i - 1

    if prev_index < 0:
        return None

    return word.sent[prev_index]


def is_cardinal(word: Token):
    """
    Determine if the input word is a cardinal number.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ == "NUM" and word.tag_ == "CD"


def is_conjunction(word: Token):
    """
    Determine if the input word has the role of conjunction.
    ("and"; "or"; ",").

    :param word: The target token.
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
    Determine if the input word is a noun.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    # TODO: add "PRON"?
    return word.pos_ in ["NOUN", "PROPN"]


def is_pronoun(word: Token):
    """
    Determine if the input word is a pronoun.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.tag_ in ["PRP", "PRP$"]


def is_nsubj_wh_word(sentence: Span, word: Token):
    """
    Check if the input word is part of a chunk which is composed by
    only a WH-word in relation of "nsubj".

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"
            * the chunk "Which" is WH-word in relation of "nsubj"

    :param sentence: The target sentence.
    :param word: The target token.
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
    Determine if the input word is a preposition.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    # TODO:
    # return word.dep_ == "prep" or len(
    #     [conj.dep_ == "prop" for conj in list(word.conjuncts)]
    # ) > 0

    return word.pos_ == "ADP" and word.tag_ == "IN"


def is_verb(word: Token):
    """
    Determine if the input word is a verb.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ in ["AUX", "VERB"]


def is_aux(word: Token):
    """
    Determine if the input word is an auxiliary verb.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    is_aux_lemma = word.lemma_.lower() in AUXILIARY_VERBS
    is_aux_verb = word.pos_ == "AUX"

    return is_aux_verb or is_aux_lemma


def is_aux_pass(word: Token):
    """
    Determine if the input word is a passive auxiliary verb.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return is_aux(word) and word.dep_ == "auxpass"


def is_adj(word: Token):
    """
    Determine if the input word is an adjective.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ == "ADJ"


def is_adj_comparative(word: Token):
    """
    Determine if the input word is a comparative adjective.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return is_adj(word) and word.tag_ == "JJR"


def is_adj_complement(word: Token):
    """
    Determine if the input word is an adjectival complement.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return is_adj(word) and word.dep_ == "acomp"


def is_adj_superlative(word: Token):
    """
    Determine if the input word is a superlative adjective.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return is_adj(word) and word.tag_ == "JJS"


def is_adj_modifier(word: Token):
    """
    Determine if the input word is an adjectival modifier.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return is_adj(word) and word.tag_ == "JJ" and word.dep_ == "amod"


def is_adv(word: Token):
    """
    Determine if the input word is an adverb.

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ == "ADV"


def is_common_det(word: Token):
    """
    Determine if the input word is a common determiner ("a", "the").

    :param word: The target token.
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

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.tag_ == 'WRB'


def is_wh_det(word: Token):
    """
    Determine if the input word is wh-determiner ("which", etc.).

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.pos_ == "DET" \
           and word.tag_ == "WDT" \
           and word.dep_ == "det"


def is_wh_word(word: Token):
    """
    Check if the input word is one of the WH-words:\n
    - when, where, why\n
    - whence, whereby, wherein, whereupon\n
    - how\n
    - what, which, whose\n
    - who, whose, which, what\n

    Resources:\n
    - https://grammar.collinsdictionary.com/easy-learning/wh-words\n
    - https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    return word.tag_ in ['WDT', 'WP', 'WP$', 'WRB']


def is_followed_by_possessive(word: Token):
    """
    Check if the input word is followed by a possessive.

    E.g.:
        - question: "Who is the person whose successor was Le Hong Phong?"

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    for right in word.sent:
        if right.i > word.i and right.dep_ == "poss":
            return True

    return False


def is_followed_by_prep(word: Token):
    """
    Determine if the input word is followed by a preposition.

    E.g.:
        - question: "Which soccer players were born on Malta?"

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return None

    next_word = get_next_word(word)

    if next_word is None:
        return False

    return next_word.dep_ == "prep"


def is_preceded_by_adj_modifier(word: Token):
    """
    Determine if the input word is preceded by an adjective modifier.

    E.g.:
        - question: "Give me all Swedish holidays."

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return None

    prev_word = get_prev_word(word)

    if prev_word is None:
        return False

    return is_adj_modifier(prev_word)


def is_preceded_by_pass(word: Token):
    """
    Determine if the input word is preceded by a passive auxiliary.

    E.g.:
        - question: ### "where was the person who won the oscar born?"

    :param word: The target token.
    :return: True/False
    """

    if not isinstance(word, Token):
        return False

    for left in list(word.lefts):
        if is_aux_pass(left) is True:
            return True

    return False

