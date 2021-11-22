import warnings
from spacy.tokens import Token

from ro.webdata.oniq.common.constants import SYSTEM_MESSAGES
from ro.webdata.oniq.nlp.word_utils import get_prev_word, is_adj, is_adv, is_common_det


# TODO: ilie.dorobat: add the documentation
def get_adv_determiner(word: Token):
    warnings.warn(SYSTEM_MESSAGES.METHOD_NOT_USED, DeprecationWarning)
    warnings.warn(SYSTEM_MESSAGES.METHOD_NOT_TESTED, DeprecationWarning)

    if not isinstance(word, Token) or not is_adv(word):
        return None

    prev_word = get_prev_word(word)
    comparison_adv = get_comparison_adv(word)

    if comparison_adv is not None:
        prev_word = get_prev_word(prev_word)

    if is_common_det(prev_word):
        return prev_word

    return None


def get_comparison_adv(word: Token = None):
    """
    Get the superlative/comparative adverb that precedes an adjective

    :param word: The target adjective
    :return: The superlative/comparative adverb that precedes an adjective
    """

    if not isinstance(word, Token) or not is_adj(word):
        return None

    prev_word = get_prev_word(word)

    # E.g.: "Did it rain most often at the beginning of the year?"
    # - "often" is adv && tag == "RB"
    # - "most" is adv && tag != "RB"
    if is_adv(prev_word) and prev_word.tag_ == "RB":
        prev_word = get_prev_word(prev_word)

    if prev_word is None or prev_word.tag_ not in ["RBR", "RBS"]:
        return None

    return prev_word
