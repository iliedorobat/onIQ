from typing import List

from spacy.tokens import Token, Span

from ro.webdata.oniq.common.nlp.utils import WordnetUtils, SENTI_WORD_TYPE
from ro.webdata.oniq.common.nlp.word_utils import is_adj, get_prev_word
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, QUESTION_TYPES
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.final_triples.Triple import Triple
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class QUERY_TYPES:
    ASK = "ASK"
    COUNT = "COUNT"
    SELECT = "SELECT"


class ORDER_BY_MODIFIER:
    ASC = "ASC"
    DESC = "DESC"


class SPARQLQuery:
    def __init__(self, nl_question: NLQuestion, targets: List[NounEntity], triples: List[Triple]):
        self.nl_question = nl_question
        self.targets = targets
        self.triples = triples
        self.query_type = _get_query_type(self.nl_question)

    def generate_query(self):
        output = ""

        if self.query_type == QUERY_TYPES.ASK:
            output = "ASK"
        else:
            output = "SELECT DISTINCT"
            for target in self.targets:
                output += f" {target.to_var()}"

        output += "\nWHERE {"
        for triple in self.triples:
            output += f"\n\t{str(triple)} ."
        output += "\n}"

        return output


class SPARQLRawQuery:
    def __init__(self, nl_question: NLQuestion, targets: List[NounEntity], raw_triples: List[RawTriple], order_by_items: List[RawTriple]):
        self.nl_question = nl_question
        self.targets = targets
        self.raw_triples = raw_triples
        self.query_type = _get_query_type(self.nl_question)
        self.order_by = OrderByClause(order_by_items)

    def generate_query(self):
        output = f'query_type = {self.query_type}\n'

        if self.query_type == QUERY_TYPES.ASK:
            output += "target_nouns = []\n"
        else:
            output += "target_nouns = [\n"
            for target in self.targets:
                output += f"\t{target.to_var()}\n"
            output += "]\n"

        # Filter order_by.items to remove the items that already exists in
        # self.raw_triples. Using "set" will change the order or elements.
        # E.g.: "Which museum in New York has the most visitors?"
        order_by_items = [item for item in self.order_by.items if item not in self.raw_triples]
        triple_list = self.raw_triples + order_by_items

        output += "raw_triples = [\n"
        for raw_triple in triple_list:
            output += f"\t<{str(raw_triple)}>\n"
        output += "]"

        if len(self.order_by.items) > 0:
            output += "\n"
            output += f"order_modifier = {self.order_by.modifier}\n"
            output += f"order_items = [\n"
            for item in self.order_by.items:
                output += f"\t{item.o.to_var()}\n"
            output += "]\n"

        return output


class OrderByClause:
    def __init__(self, order_by_items: List[RawTriple]):
        self.items = order_by_items
        self.modifier = self._get_modifier()

    def _get_modifier(self):
        print()
        for item in self.items:
            predicate = None

            if isinstance(item.p, Span):
                predicate = item.p.root
            elif isinstance(item.p, Token):
                predicate = item.p

            if isinstance(predicate, Token):
                if is_adj(predicate):
                    # E.g.: "What is the highest mountain in Italy?"
                    return _get_order_modifier(predicate)
                else:
                    prev_word = get_prev_word(predicate)
                    # E.g.: "Which museum in New York has the fewest visitors?"
                    return _get_order_modifier(prev_word)
        return ORDER_BY_MODIFIER.ASC


def _get_order_modifier(word: Token):
    if isinstance(word, Token):
        if is_adj(word):
            senti_word_type = WordnetUtils.senti_word_analysis(word.text)

            if senti_word_type == SENTI_WORD_TYPE.POSITIVE:
                return ORDER_BY_MODIFIER.DESC

    return ORDER_BY_MODIFIER.ASC


def _get_query_type(nl_question):
    if nl_question.main_type == QUESTION_TYPES.AUX_ASK:
        return QUERY_TYPES.ASK
    elif nl_question.main_type == QUESTION_TYPES.HOW:
        return QUERY_TYPES.COUNT

    return QUERY_TYPES.SELECT
