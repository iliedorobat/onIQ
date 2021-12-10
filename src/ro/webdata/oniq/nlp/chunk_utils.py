from spacy.tokens import Span
from ro.webdata.oniq.nlp.adv_utils import get_comparison_adv, is_adv
from ro.webdata.oniq.nlp.word_utils import get_prev_word, is_common_det, is_linked_by_conjunction


def extract_comparison_adv(chunk: Span):
    """
    Get the superlative/comparative adverb that precedes the chunk

    E.g.: "Which is the noisiest, the most beautiful and the largest city?"

    :param chunk: The target chunk
    :return: The superlative/comparative adverb that precedes the chunk
    """

    if not isinstance(chunk, Span):
        return None

    return get_comparison_adv(chunk[0])


def extract_determiner(chunk: Span):
    """
    Get the determiner placed before a noun chunk

    :param chunk: The target noun chunk
    :return: The determiner
    """

    if not isinstance(chunk, Span):
        return None

    prev_word = get_prev_word(chunk[0])
    while prev_word is not None and is_adv(prev_word):
        prev_word = get_prev_word(prev_word)

    if prev_word is None or not is_common_det(prev_word):
        return None

    return prev_word


def get_first_word(chunk: Span):
    """
    Get the first word from a chunk

    :param chunk: The target noun chunk
    :return: The determiner
    """

    if not isinstance(chunk, Span) or len(chunk) == 0:
        return None

    return chunk[0]


def is_linked_chunk(chunk: Span):
    """
    Determine if the input chunk is preceded or followed by a conjunction

    :param chunk: The target chunk
    :return: True/False
    """

    if not isinstance(chunk, Span):
        return False

    return is_linked_by_conjunction(chunk[0])
