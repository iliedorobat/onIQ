from spacy.tokens import Span, Token
from ro.webdata.oniq.model.sentence.Adjective import Adjective
from ro.webdata.oniq.nlp.word_utils import is_adj, is_followed_by_conjunction, is_noun, \
    is_preceded_by_conjunction, is_verb


# E.g.: "Which of the smart kids are famous?"
# E.g.: "Which woman is beautiful, generous, tall and rich?"
def get_next_linked_adj_list(chunk: Span):
    """TODO: ilie.dorobat: update the documentation
    Get the next adjective linked to the chunk by a conjunction

    E.g.:
        - "Which of the smart kids are famous?"
            - chunk (noun chunk): "which of the smart kids"
            - next adjectives linked: ["famous"]
        - "Which woman is beautiful, generous, tall and rich?"
            - chunk (noun chunk): "Which woman"
            - next adjective linked: ["beautiful", "generous", "tall", "rich"]

    :param chunk: The target chunk
    :return: The list of adjectives found
    """

    adj_list = []

    if not isinstance(chunk, Span):
        return adj_list

    next_adj = _get_next_adj(chunk.root)
    while next_adj is not None:
        adj_list.append(next_adj)
        next_adj = _get_next_linked_adj(chunk, next_adj)

    return [Adjective(adj) for adj in adj_list]


def _get_next_linked_adj(chunk: Span, word: Token):
    """
    Get the next adjective linked to the chunk by a conjunction

    E.g.: "Which is the noisiest and the largest city?"
        - chunk (noun chunk): "the largest city"
        - previous adjective linked: "noisiest"

    :param chunk: The target chunk
    # :param word: The word from which iterates backwards
    :return: The first adjective found
    """

    if not isinstance(chunk, Span) \
            or not isinstance(word, Token) \
            or not (is_noun(word) or is_adj(word)):
        return None

    if is_followed_by_conjunction(word):
        next_adj = _get_next_adj(word)
        if next_adj not in chunk:
            return next_adj

    return None


def _count_root_verbs_passed(word: Token):
    """
    Determine how many root verbs are before the target adjective

    E.g.:
        - "How long does the museum remain closed?"
            - "does".pos_ == "AUX"      "does".pos_ == "aux"
            - "remain".pos_ == "VERB"   "remain".pos_ == "ROOT"
        - "Which of the smart kids are famous?"
            - "are".pos_ == "AUX"       "are".dep_ == "ROOT"

    :param word: The target adjective
    :return: Total number of root verbs
    """

    num = 0

    if not isinstance(word, Token):
        return num

    for index, token in list(enumerate(word.sent)):
        if index < word.i:
            # 1. "Who is very beautiful?
            # 2. "How long does the museum remain closed?"
            if is_verb(token) and token.dep_ == "ROOT":
                num += 1

    return num


def _get_prev_linked_adj(chunk: Span, word: Token):
    """
    Get the previous adjective linked to the chunk by a conjunction

    E.g.: "Which is the noisiest and the largest city?"
        - chunk (noun chunk): "the largest city"
        - previous adjective linked: "noisiest"

    :param chunk: The target chunk
    :param word: The word from which iterates backwards
    :return: The first adjective found
    """

    if not isinstance(chunk, Span) \
            or not isinstance(word, Token) \
            or not (is_noun(word) or is_adj(word)):
        return None

    if is_preceded_by_conjunction(word):
        return _get_prev_adj(chunk, word)

    return None


def get_prev_linked_adj_list(chunk: Span):
    """
    Get the previous adjectives linked to the chunk by a conjunction

    E.g.: "Which is the noisiest, the newest, the largest and the most crowded city?"
        - chunk (noun chunk): "the largest city"
        - the list of previous linked adjectives: ["noisiest", "newest", "largest"]

    :param chunk: The target chunk
    :return: The list of adjectives found
    """

    adj_list = []

    if not isinstance(chunk, Span):
        return adj_list

    prev_adj = _get_prev_linked_adj(chunk, chunk.root)
    while prev_adj is not None:
        adj_list.append(prev_adj)
        prev_adj = _get_prev_linked_adj(chunk, prev_adj)

    return [Adjective(adj) for adj in adj_list]


# TODO: ilie.dorobat: add the documentation
def _get_next_adj(word: Token):
    if not isinstance(word, Token):
        return None

    for index, token in list(enumerate(word.sent)):
        if index > word.i:
            if is_adj(token):
                # E.g.: "Which of the smart kids are famous?"
                # => "smart" is linked to "which" and has to be ignored
                if _count_root_verbs_passed(token) == 1:
                    return token

    return None


# TODO: ilie.dorobat: add the documentation
# E.g.: "Who is very beautiful and very smart?"
def _get_prev_adj(chunk: Span, word: Token):
    if not isinstance(chunk, Span) or not isinstance(word, Token):
        return None

    for index, token in list(reversed(list(enumerate(word.sent)))):
        if index < word.i:
            if is_adj(token) and token not in chunk:
                return token
            elif is_verb(token):
                return None

    return None
