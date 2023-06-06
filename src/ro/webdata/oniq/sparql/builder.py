import json
from typing import List

import pydash
import requests
from spacy.tokens import Span

from ro.webdata.oniq.common.nlp.sentence_utils import get_root
from ro.webdata.oniq.common.nlp.word_utils import get_prev_word, is_adj
from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_RESOURCE_TYPE_QUERY, DBP_ENDPOINT
from ro.webdata.oniq.endpoint.models.RDFElement import URI, URI_TYPE
from ro.webdata.oniq.endpoint.query import QueryService
from ro.webdata.oniq.service.query_const import ACCESSORS, PATHS
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, ROOT_TYPES, QUESTION_TARGET
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.final_triples.Triple import Triple
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.model.raw_triples.raw_target_utils import RawTargetUtils
from ro.webdata.oniq.sparql.model.raw_triples.raw_triple_utils import RawTripleUtils
from ro.webdata.oniq.sparql.query import SPARQLQuery, SPARQLRawQuery


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


class SPARQLBuilder(SPARQLRawBuilder):
    def __init__(self, endpoint, input_question, print_deps):
        super().__init__(endpoint, input_question, print_deps)
        self.triples = _init_triples(self.raw_triples)

    def to_sparql_query(self):
        query = SPARQLQuery(self.nl_question, self.targets, self.triples)
        return query.generate_query()


def _get_entities(question: str):
    entities_uri = f'http://localhost:8200/{PATHS.ENTITIES}?{ACCESSORS.QUESTION}={question}'
    entities_response = requests.get(entities_uri)
    return json.loads(entities_response.content)


def _init_triples(raw_triples: List[RawTriple]):
    triples = []

    for raw_triple in raw_triples:
        triple = Triple(raw_triple)
        triples.append(triple)

    return triples


def _prepare_raw_triples(nl_question: NLQuestion):
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

    _update_location_triple(raw_triples)
    _update_awards_triple(raw_triples)

    return raw_triples


def _prepare_target_nouns(nl_question: NLQuestion, raw_triples: List[RawTriple]):
    target_nouns = []

    for raw_triple in raw_triples:
        RawTargetUtils.update_target_nouns(nl_question, target_nouns, raw_triple)

    return target_nouns


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
