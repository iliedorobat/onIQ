import json
from typing import List, Union

import pydash
import requests
from spacy.tokens import Span, Token

from ro.webdata.oniq.endpoint.models.RDFElement import URI_TYPE
from ro.webdata.oniq.service.query_const import PATHS, ACCESSORS
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, ANSWER_TYPE
from ro.webdata.oniq.sparql.model.triples.RawTriple import RawTriple


def get_improved_raw_triples(raw_triples: List[RawTriple], nl_question: NLQuestion):
    temp_p_list = []
    output = []

    for triple in raw_triples:
        predicate = triple.p

        if "dbo:birthDate" not in temp_p_list:
            predicate = _get_age_predicate(triple, nl_question, predicate)
        if "dbo:elevation" not in temp_p_list:
            predicate = _get_mountain_predicate(raw_triples, triple, predicate)
        if "dbo:locatedInArea" not in temp_p_list:
            if isinstance(triple.o.token, Token) and triple.o.token.ent_type_ in ["GPE", "LOC"]:
                # E.g.: "Which volcanos in Japan erupted since 2000?"
                predicate = _update_location_triple(raw_triples, predicate)

        temp_p_list.append(
            str(predicate)
        )
        output.append(
            RawTriple(triple.s, predicate, triple.o, triple.question, triple.order_by)
        )

    return output


def _get_age_predicate(triple: RawTriple, nl_question: NLQuestion, predicate: Union[str, Span]):
    if nl_question.answer_type == ANSWER_TYPE.PERSON:
        if isinstance(triple.p, Span) and triple.p.root.lemma_ in ["old", "young"]:
            # E.g.: "Who is the youngest Pulitzer Prize winner?"
            return "dbo:birthDate"

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
