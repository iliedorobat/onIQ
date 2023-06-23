import json
from typing import List, Union

import pydash
import requests
from spacy.tokens import Span

from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_ENDPOINT, DBP_RESOURCE_TYPE_QUERY
from ro.webdata.oniq.endpoint.models.RDFElement import URI, URI_TYPE
from ro.webdata.oniq.endpoint.query import QueryService
from ro.webdata.oniq.service.query_const import PATHS, ACCESSORS
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, QUESTION_TARGET
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


def get_improved_raw_triples(raw_triples: List[RawTriple], nl_question: NLQuestion):
    temp_p_list = []
    output = []

    for triple in raw_triples:
        predicate = triple.p

        if "dbo:birthDate" not in temp_p_list:
            predicate = _get_age_predicate(triple, nl_question, predicate)
        if "dbo:award" not in temp_p_list:
            predicate = _get_awards_predicate(triple, predicate)
        if "dbo:elevation" not in temp_p_list:
            predicate = _get_mountain_predicate(raw_triples, triple, predicate)
        if "dbo:locatedInArea" not in temp_p_list:
            predicate = _update_location_triple(raw_triples, predicate)

        temp_p_list.append(
            str(predicate)
        )
        output.append(
            RawTriple(triple.s, predicate, triple.o, triple.question, triple.order_by)
        )

    return output


def _get_age_predicate(triple: RawTriple, nl_question: NLQuestion, predicate: Union[str, Span]):
    is_person = QUESTION_TARGET.PERSON

    if nl_question.target == is_person:
        if isinstance(triple.p, Span) and triple.p.root.lemma_ in ["old", "young"]:
            # E.g.: "Who is the youngest Pulitzer Prize winner?"
            return "dbo:birthDate"

    return predicate


def _get_awards_predicate(triple: RawTriple, predicate: Union[str, Span]):
    # Get "dbo:award" predicate if the triple contains an Award triple object
    # E.g.: "Who is the youngest Pulitzer Prize winner?"

    if triple.o.is_res():
        obj_var = triple.o.to_var()
        resource_name = obj_var.replace("dbr:", "")

        parent_classes = QueryService.run_resource_type_query(DBP_ENDPOINT, resource_name, DBP_RESOURCE_TYPE_QUERY)
        is_award = URI.AWARD_CLASS in parent_classes

        if is_award:
            return "dbo:award"

    return predicate


def _get_mountain_predicate(raw_triples: List[RawTriple], triple: RawTriple, predicate: Union[str, Span]):
    exists_mountain: bool = len([
        triple for triple in raw_triples
        if triple.is_dbo_mountain_type()
    ]) > 0

    if exists_mountain:
        if isinstance(triple.p, Span) and triple.p.root.lemma_ == "high":
            # E.g.: "What is the highest mountain in Italy?"
            return "dbo:elevation"

    return predicate


def _update_location_triple(raw_triples: List[RawTriple], predicate: Union[str, Span]):
    # Get "dbo:locatedInArea" if the triple contains a Natural Place triple object
    # E.g.: "What is the highest mountain in Italy?"

    rdf_type_triples: List[RawTriple] = [
        triple for triple in raw_triples
        if triple.is_rdf_type()
    ]

    # E.g.: <?mountain   rdf:type   dbo:Mountain>
    rdf_type_triple: RawTriple = pydash.get(rdf_type_triples, "0")

    if rdf_type_triple is not None:
        obj_var = rdf_type_triple.o.to_var()
        resource_type_uri = f'http://localhost:8200/{PATHS.RESOURCE_TYPE}?{ACCESSORS.RESOURCE_NAME}={obj_var}'

        resource_type_response = requests.get(resource_type_uri)
        resource_type: str = json.loads(resource_type_response.content)

        if resource_type == URI_TYPE.NATURAL_PLACE:
            return "dbo:locatedInArea"

    return predicate
