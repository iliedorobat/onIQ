from typing import Union

from spacy.tokens import Token

from ro.webdata.oniq.common.nlp.utils import WordnetUtils, SENTI_WORD_TYPE
from ro.webdata.oniq.common.nlp.word_utils import is_adj, get_prev_word
from ro.webdata.oniq.sparql.model.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity


class ORDER_BY_MODIFIER:
    ASC = "ASC"
    DESC = "DESC"


class OrderBy:
    def __init__(self, target: Union[AdjectiveEntity, NounEntity], predicate: Token):
        self.target = target
        self.modifier = OrderBy.get_modifier(predicate)

    @staticmethod
    def get_modifier(predicate: Token):
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
            if word.lower_ == "most":
                return ORDER_BY_MODIFIER.DESC
            elif word.lower_ == "least":
                return ORDER_BY_MODIFIER.ASC
            else:
                senti_word_type = WordnetUtils.senti_word_analysis(word.text)

                if senti_word_type == SENTI_WORD_TYPE.POSITIVE:
                    return ORDER_BY_MODIFIER.DESC

    return ORDER_BY_MODIFIER.ASC
