from typing import Union

from spacy.tokens import Token

from ro.webdata.oniq.common.nlp.utils import WordnetUtils, SENTI_WORD_TYPE
from ro.webdata.oniq.common.nlp.word_utils import is_adj, get_prev_word
from ro.webdata.oniq.sparql.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.NounEntity import NounEntity


class ORDER_BY_MODIFIER:
    ASC = "ASC"
    DESC = "DESC"


class OrderBy:
    def __init__(self, target: Union[AdjectiveEntity, NounEntity], predicate: Token, order_adj: Token = None):
        self.target = target
        self.modifier = OrderBy.get_modifier(predicate, order_adj)
        self.order_by_token = order_adj if is_adj(order_adj) else predicate

    def __str__(self):
        prev_word = get_prev_word(self.target.token)

        if prev_word.lower_ in ["most", "least"]:
            # E.g.: "Which musician wrote the most books?"
            return f"{self.modifier}(COUNT({self.target.to_var()}))"

        return f"{self.modifier}({self.target.to_var()})"

    @staticmethod
    def get_modifier(predicate: Token, order_adj: Token = None):
        if not isinstance(predicate, Token):
            return None

        if is_adj(predicate):
            # E.g.: "What is the highest mountain in Italy?"
            return _prepare_order_modifier(predicate)
        elif is_adj(order_adj):
            # E.g.: "What is the smallest city by area in Germany?"
            return _prepare_order_modifier(order_adj)
        else:
            # E.g.: "Which museum in New York has the fewest visitors?"
            prev_word = get_prev_word(predicate)
            return _prepare_order_modifier(prev_word)


def _prepare_order_modifier(word: Token):
    if isinstance(word, Token):
        if is_adj(word):
            if word.lemma_ in ["most", "young"]:
                return ORDER_BY_MODIFIER.DESC
            elif word.lemma_ in ["least", "old"]:
                return ORDER_BY_MODIFIER.ASC
            else:
                senti_word_type = WordnetUtils.senti_word_analysis(word.text)

                if senti_word_type == SENTI_WORD_TYPE.POSITIVE:
                    return ORDER_BY_MODIFIER.DESC

    return ORDER_BY_MODIFIER.ASC
