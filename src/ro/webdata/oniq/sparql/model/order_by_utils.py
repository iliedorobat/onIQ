from typing import Union

from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.utils import WordnetUtils, SENTI_WORD_TYPE
from ro.webdata.oniq.common.nlp.word_utils import is_adj, get_prev_word


class ORDER_BY_MODIFIER:
    ASC = "ASC"
    DESC = "DESC"


def get_order_modifier(predicate: Token):
    if not isinstance(predicate, Token):
        return None

    if is_adj(predicate):
        # E.g.: "What is the highest mountain in Italy?"
        return _prepare_order_modifier(predicate)
    else:
        # E.g.: "Which museum in New York has the fewest visitors?"
        prev_word = get_prev_word(predicate)
        return _prepare_order_modifier(prev_word)


def _prepare_order_modifier(word: Token):
    if isinstance(word, Token):
        if is_adj(word):
            senti_word_type = WordnetUtils.senti_word_analysis(word.text)

            if senti_word_type == SENTI_WORD_TYPE.POSITIVE:
                return ORDER_BY_MODIFIER.DESC

    return ORDER_BY_MODIFIER.ASC
