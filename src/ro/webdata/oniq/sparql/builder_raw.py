import json
from typing import List

import pydash
import requests
from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.nlp_utils import token_to_span
from ro.webdata.oniq.common.nlp.sentence_utils import get_root
from ro.webdata.oniq.common.nlp.word_utils import get_prev_word, is_adj
from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_RESOURCE_TYPE_QUERY, DBP_ENDPOINT
from ro.webdata.oniq.endpoint.models.RDFElement import URI, URI_TYPE
from ro.webdata.oniq.endpoint.query import QueryService
from ro.webdata.oniq.service.query_const import ACCESSORS, PATHS
from ro.webdata.oniq.sparql.model.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, SYNTACTIC_TYPES, QUESTION_TYPES, QUESTION_TARGET
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.OrderBy import OrderBy
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.model.raw_triples.raw_target_utils import RawTargetUtils
from ro.webdata.oniq.sparql.model.raw_triples.raw_triple_utils import WRawTripleUtils, HRawTripleUtils
from ro.webdata.oniq.sparql.query import SPARQLRawQuery


class SPARQLRawBuilder:
    def __init__(self, endpoint, input_question, print_deps):
        self.nl_question = NLQuestion(input_question)
        self.raw_triples = _prepare_raw_triples(self.nl_question)
        self.targets = _prepare_target_nouns(self.nl_question, self.raw_triples)

        if print_deps:
            echo.deps_list(self.nl_question.question)

    def to_sparql_query(self):
        query = SPARQLRawQuery(self.nl_question, self.targets, self.raw_triples)
        return query.generate_query()


def _prepare_raw_triples(nl_question: NLQuestion):
    initial_triples = _init_raw_triples(nl_question)

    order_by_triples = _prepare_ordering_raw_triples(nl_question, initial_triples)
    # Exclude the triples used in the ORDER BY statement.
    # Using "set" will change the order or elements.
    # E.g.: "Which museum in New York has the most visitors?"
    main_triples = [raw_triple for raw_triple in initial_triples if raw_triple not in order_by_triples]

    return main_triples + order_by_triples


def _init_raw_triples(nl_question: NLQuestion):
    root = get_root(nl_question.question)
    syntactic_type = nl_question.syntactic_type
    question_type = nl_question.question_type
    raw_triples = []

    if question_type == QUESTION_TYPES.HOW:
        # E.g.: "How high is the Yokohama Marine Tower?"
        HRawTripleUtils.aux_processing(nl_question, raw_triples, root)
    else:
        if syntactic_type == SYNTACTIC_TYPES.S_AUX:
            WRawTripleUtils.aux_ask_processing(nl_question, raw_triples, root)
        if syntactic_type == SYNTACTIC_TYPES.S_VERB:
            WRawTripleUtils.verb_ask(nl_question, raw_triples, root)
        elif syntactic_type == SYNTACTIC_TYPES.S_NOUN:
            WRawTripleUtils.noun_ask(nl_question, raw_triples, root)
        elif syntactic_type == SYNTACTIC_TYPES.S_PREP:
            WRawTripleUtils.prep_ask_processing(nl_question, raw_triples, root)
        elif syntactic_type == SYNTACTIC_TYPES.PASSIVE:
            WRawTripleUtils.passive_processing(nl_question, raw_triples, root)
        elif syntactic_type == SYNTACTIC_TYPES.PASSIVE_NEAR:
            WRawTripleUtils.passive_near_processing(nl_question, raw_triples, root)
        elif syntactic_type == SYNTACTIC_TYPES.POSSESSIVE:
            WRawTripleUtils.possessive_processing(nl_question, raw_triples, root)
        elif syntactic_type == SYNTACTIC_TYPES.POSSESSIVE_COMPLEX:
            WRawTripleUtils.possessive_complex_processing(nl_question, raw_triples, root)
        elif syntactic_type == SYNTACTIC_TYPES.AUX:
            WRawTripleUtils.aux_processing(nl_question, raw_triples, root)
        elif syntactic_type == SYNTACTIC_TYPES.MAIN:
            WRawTripleUtils.main_processing(nl_question, raw_triples, root)
        else:
            print(f"The question \"{nl_question.question}\" cannot be parsed!")

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
        if triple.is_location()
    ]
    rdf_type_triples: List[RawTriple] = [
        triple for triple in raw_triples
        if triple.is_rdf_type()
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


def _prepare_target_nouns(nl_question: NLQuestion, raw_triples: List[RawTriple]):
    target_nouns = []

    for raw_triple in raw_triples:
        RawTargetUtils.update_target_nouns(nl_question, target_nouns, raw_triple)

    return target_nouns


def _prepare_ordering_raw_triples(nl_question: NLQuestion, raw_triples: List[RawTriple]):
    order_by = []

    for raw_triple in raw_triples:
        obj_span = raw_triple.o.to_span()
        prev_word = get_prev_word(obj_span[0]) \
            if obj_span is not None \
            else None

        if isinstance(prev_word, Token):
            if raw_triple.s.is_var():
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

            elif raw_triple.o.is_var():
                # E.g.: "Who is the oldest child of Meryl Streep?"

                if is_adj(prev_word):
                    obj = AdjectiveEntity(prev_word)
                    new_raw_triple = RawTriple(
                        s=raw_triple.o,
                        p=token_to_span(prev_word),
                        o=obj,
                        question=nl_question.question,
                        order_by=OrderBy(obj, prev_word)
                    )
                    order_by.append(new_raw_triple)

    _update_mountain_triple(order_by, raw_triples)
    _update_age_triple(order_by, nl_question)

    return order_by


def _update_mountain_triple(order_by_triples: List[RawTriple], main_triples: List[RawTriple]):
    is_mountain: bool = len([
        triple for triple in main_triples
        if triple.is_dbo_mountain_type()
    ]) > 0

    if is_mountain:
        for triple in order_by_triples:
            if isinstance(triple.p, Span) and triple.p.root.lemma_ == "high":
                # E.g.: "What is the highest mountain in Italy?"
                triple.p = "dbo:elevation"


def _update_age_triple(order_by_triples: List[RawTriple], nl_question: NLQuestion):
    is_person = QUESTION_TARGET.PERSON

    if nl_question.target == is_person:
        for triple in order_by_triples:
            if isinstance(triple.p, Span) and triple.p.root.lemma_ in ["old", "young"]:
                # E.g.: "Who is the youngest Pulitzer Prize winner?"
                triple.p = "dbo:birthDate"
