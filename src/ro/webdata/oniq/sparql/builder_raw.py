import json
from typing import List

import pydash
import requests

from ro.webdata.oniq.common.nlp.sentence_utils import get_root
from ro.webdata.oniq.common.nlp.word_utils import get_prev_word, is_adj
from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_RESOURCE_TYPE_QUERY, DBP_ENDPOINT
from ro.webdata.oniq.endpoint.models.RDFElement import URI, URI_TYPE
from ro.webdata.oniq.endpoint.query import QueryService
from ro.webdata.oniq.service.query_const import ACCESSORS, PATHS
from ro.webdata.oniq.sparql.model.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, ROOT_TYPES, QUESTION_TARGET
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.model.raw_triples.raw_target_utils import RawTargetUtils
from ro.webdata.oniq.sparql.model.raw_triples.raw_triple_utils import RawTripleUtils
from ro.webdata.oniq.sparql.query import SPARQLRawQuery


class SPARQLRawBuilder:
    def __init__(self, endpoint, input_question, print_deps):
        self.nl_question = NLQuestion(input_question)
        initial_triples = _init_raw_triples(self.nl_question)

        self.order_by_triples = _prepare_ordering_raw_triples(self.nl_question, initial_triples)
        self.main_triples = _get_main_raw_triples(initial_triples, self.order_by_triples)
        self.all_triples = self.main_triples + self.order_by_triples
        self.targets = _prepare_target_nouns(self.nl_question, self.all_triples)

        if print_deps:
            echo.deps_list(self.nl_question.question)

    def to_sparql_query(self):
        query = SPARQLRawQuery(self.nl_question, self.targets, self.all_triples, self.order_by_triples)
        return query.generate_query()


def _init_raw_triples(nl_question: NLQuestion):
    root = get_root(nl_question.question)
    root_type = nl_question.root_type
    raw_triples = []

    if root_type == ROOT_TYPES.AUX_ASK:
        RawTripleUtils.aux_ask_processing(nl_question, raw_triples, root)
    if root_type == ROOT_TYPES.VERB_ASK:
        RawTripleUtils.verb_ask(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.PREP_ASK:
        RawTripleUtils.prep_ask_processing(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.PASSIVE:
        RawTripleUtils.passive_processing(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.POSSESSIVE:
        RawTripleUtils.possessive_processing(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.POSSESSIVE_COMPLEX:
        RawTripleUtils.possessive_complex_processing(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.AUX:
        RawTripleUtils.aux_processing(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.MAIN:
        RawTripleUtils.main_processing(nl_question, raw_triples, root)
    else:
        # subject = root
        # predicate = get_related_verb(subject, sentence[subject.i + 1:])
        # obj = get_child_noun(predicate, sentence[predicate.i:])
        # triple = self.triples.append_triple(subject, predicate, obj)
        pass

    _update_awards_triple(raw_triples)
    _update_location_triple(raw_triples)

    return raw_triples


def _update_awards_triple(raw_triples: List[RawTriple]):
    # Change the triple predicate with "award" predicate if the triple list
    # contains an Award triple object
    # E.g.: "Who is the youngest Pulitzer Prize winner?"

    for triple in raw_triples:
        if triple.o.is_res():
            obj_var = triple.o.to_var()
            resource_name = obj_var.replace("dbr:", "")

            parent_classes = QueryService.run_resource_type_query(DBP_ENDPOINT, resource_name, DBP_RESOURCE_TYPE_QUERY)
            is_award = URI.AWARD_CLASS in parent_classes

            if is_award:
                triple.p = "award"


def _update_location_triple(raw_triples: List[RawTriple]):
    # Change the "location" predicate with "locatedInArea" if the triple list
    # contains a Natural Place triple object
    # E.g.: "What is the highest mountain in Italy?"

    loc_triples: List[RawTriple] = [
        triple for triple in raw_triples
        if isinstance(triple.p, str) and triple.p == QUESTION_TARGET.LOCATION
    ]
    rdf_type_triples: List[RawTriple] = [
        triple for triple in raw_triples
        if isinstance(triple.p, str) and triple.p == "rdf:type"
    ]

    # E.g.: <?mountain   location   dbr:Italy>
    loc_triple: RawTriple = pydash.get(loc_triples, "0")
    # E.g.: <?mountain   rdf:type   dbo:Mountain>
    rdf_type_triple: RawTriple = pydash.get(rdf_type_triples, "0")

    if loc_triple is not None and rdf_type_triple is not None:
        obj_var = rdf_type_triple.o.to_var()
        resource_type_uri = f'http://localhost:8200/{PATHS.RESOURCE_TYPE}?{ACCESSORS.RESOURCE_NAME}={obj_var}'

        resource_type_response = requests.get(resource_type_uri)
        resource_type: str = json.loads(resource_type_response.content)

        if resource_type == URI_TYPE.NATURAL_PLACE:
            loc_triple.p = "locatedInArea"


def _get_main_raw_triples(init_raw_triples: List[RawTriple], order_by_raw_triples: List[RawTriple]):
    # Exclude the triples used in the ORDER BY statement.
    # Using "set" will change the order or elements.
    # E.g.: "Which museum in New York has the most visitors?"

    return [raw_triple for raw_triple in init_raw_triples if raw_triple not in order_by_raw_triples]


def _prepare_target_nouns(nl_question: NLQuestion, raw_triples: List[RawTriple]):
    target_nouns = []

    for raw_triple in raw_triples:
        RawTargetUtils.update_target_nouns(nl_question, target_nouns, raw_triple)

    return target_nouns


def _prepare_ordering_raw_triples(nl_question: NLQuestion, raw_triples: List[RawTriple]):
    order_by = []

    for raw_triple in raw_triples:
        obj_span = raw_triple.o.to_span()

        if obj_span is not None:
            prev_word = get_prev_word(obj_span[0])

            if raw_triple.s.is_var():
                if prev_word.text.lower() in ["most", "least"]:
                    # E.g.: "Which museum in New York has the most visitors?"
                    order_by.append(raw_triple)

                elif is_adj(prev_word):
                    if raw_triple.o.is_res():
                        # E.g.: "Who is the youngest Pulitzer Prize winner?"
                        new_raw_triple = RawTriple(
                            s=raw_triple.s,
                            p=prev_word,
                            o=AdjectiveEntity(prev_word),
                            question=nl_question.question
                        )
                        order_by.append(new_raw_triple)
                    else:
                        if raw_triple.o.is_dbpedia_type:
                            if NounEntity(prev_word).is_res():
                                # Do nothing
                                # E.g.: "Give me all Swedish holidays."
                                pass
                            else:
                                # E.g.: "Which museum in New York has the fewest visitors?"
                                new_raw_triple = RawTriple(
                                    s=raw_triple.s,
                                    p=prev_word,
                                    o=AdjectiveEntity(prev_word),
                                    question=nl_question.question
                                )
                                order_by.append(new_raw_triple)

            elif raw_triple.o.is_var():
                # E.g.: "Who is the oldest child of Meryl Streep?"

                if is_adj(prev_word):
                    new_raw_triple = RawTriple(
                        s=raw_triple.o,
                        p=prev_word,
                        o=AdjectiveEntity(prev_word),
                        question=nl_question.question
                    )
                    order_by.append(new_raw_triple)

    return order_by
