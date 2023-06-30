from typing import List

from spacy.tokens import Token

from ro.webdata.oniq.common.nlp.nlp_utils import token_to_span
from ro.webdata.oniq.common.nlp.word_utils import get_prev_word, is_adj
from ro.webdata.oniq.sparql.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.NLQuestion import NLQuestion
from ro.webdata.oniq.sparql.NounEntity import NounEntity
from ro.webdata.oniq.sparql.order.OrderBy import OrderBy
from ro.webdata.oniq.sparql.triples.raw_triples.RawTriple import RawTriple


class OrderByRawTriple:
    @staticmethod
    def prepare_extra_raw_triples(nl_question: NLQuestion, raw_triples_values: List[RawTriple]):
        order_by = []

        for raw_triple in raw_triples_values:
            obj_span = raw_triple.o.to_span()
            prev_word = get_prev_word(obj_span[0]) \
                if obj_span is not None \
                else None

            if isinstance(prev_word, Token):
                if raw_triple.s.is_var():
                    if is_adj(raw_triple.s.token):
                        raw_triple.order_by = OrderBy(raw_triple.s, raw_triple.s.token)

                    if prev_word.lower_ in ["most", "least"]:
                        if raw_triple.o.is_dbpedia_type:
                            # E.g.: "Which musician wrote the most books?"
                            raw_triple.order_by = OrderBy(raw_triple.s, prev_word)
                        else:
                            # E.g.: "Which museum in New York has the most visitors?"
                            raw_triple.order_by = OrderBy(raw_triple.o, prev_word)
                        order_by.append(raw_triple)

                    elif is_adj(prev_word):
                        is_res = raw_triple.o.is_res()
                        is_dbpedia_type = raw_triple.o.is_dbpedia_type
                        prev_word_is_res = NounEntity(prev_word).is_res()

                        if is_res or (is_dbpedia_type and not prev_word_is_res):
                            # E.g.: is_res => "Who is the youngest Pulitzer Prize winner?"
                            # E.g.: is_dbpedia_type => "Which museum in New York has the fewest visitors?"
                            # E.g.: is_dbpedia_type => "What is the highest mountain in Italy?"
                            # E.g.: prev_word_is_res => "Give me all Swedish holidays."

                            obj = AdjectiveEntity(prev_word)
                            new_raw_triple = RawTriple(
                                s=raw_triple.s,
                                p=token_to_span(prev_word),
                                o=obj,
                                question=nl_question.question,
                                order_by=OrderBy(obj, prev_word)
                            )
                            order_by.append(new_raw_triple)

                if raw_triple.o.is_var():
                    if is_adj(raw_triple.o.token):
                        # E.g.: "What is the highest mountain in Italy?"
                        raw_triple.order_by = OrderBy(raw_triple.o, raw_triple.o.token)

                    if prev_word.lower_ not in ["most", "least"]:
                        # E.g.: "Which museum in New York has the most visitors?"
                        # => prev_word.lower_ in ["most", "least"]
                        if is_adj(prev_word):
                            # E.g.: "Who is the oldest child of Meryl Streep?"
                            obj = AdjectiveEntity(prev_word)
                            new_raw_triple = RawTriple(
                                s=raw_triple.o,
                                p=token_to_span(prev_word),
                                o=obj,
                                question=nl_question.question,
                                order_by=OrderBy(obj, prev_word)
                            )
                            order_by.append(new_raw_triple)

        return order_by
