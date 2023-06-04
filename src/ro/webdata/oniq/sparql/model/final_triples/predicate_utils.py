import json
from typing import Union

import requests
from spacy.tokens import Span

from ro.webdata.oniq.common.nlp.nlp_utils import text_to_span
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.models.RDFElement import RDFProperty
from ro.webdata.oniq.service.query_const import PATHS, ACCESSORS, DATA_TYPE, NODE_TYPE
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity


def object_predicate_lookup(question: Span, obj: NounEntity, predicate: Span):
    if isinstance(predicate, Span):
        # E.g.: "Who is the youngest Pulitzer Prize winner?"
        #       <?person   winner   dbr:Pulitzer_Prize>
        return _span_lookup(
            question=question,
            predicate=predicate,
            node_type=NODE_TYPE.OBJECT,
            node_value=obj
        )

    elif isinstance(predicate, str):
        # E.g.: "Give me all Swedish holidays."
        #       <?holiday   "country"   dbr:Sweden>

        # E.g.: "Give me all ESA astronauts."
        #       <?astronaut   ?prop   dbr:ESA>
        return _string_lookup(
            question=question,
            predicate=predicate,
            node_type=NODE_TYPE.OBJECT,
            node_value=obj
        )

    return predicate


def subject_predicate_lookup(question: Span, subject: NounEntity, predicate: Union[str, Span], obj: NounEntity):
    if isinstance(predicate, Span):
        if predicate.text.lower() == "attend":
            # E.g.: "Did Arnold Schwarzenegger attend a university?"
            if obj.text is not None and "university" in obj.text.lower():
                return "dbo:almaMater"

        # TODO: move the exception to MatcherHandler => update PropertiesMatcher.get_best_matched
        #  to accept an array of target_expression
        if predicate.text.lower() == "dissolve":
            # Use a proper synonym for the word "dissolve"
            # E.g.: "When did the Ming dynasty dissolve?"
            return _string_lookup(
                question=question,
                predicate="end",
                node_type=NODE_TYPE.SUBJECT,
                node_value=subject
            )

        # E.g.: "In which country is Mecca located?"
        #       <dbr:Mecca   country   ?country>
        return _span_lookup(
            question=question,
            predicate=predicate,
            node_type=NODE_TYPE.SUBJECT,
            node_value=subject
        )

    return predicate


def _span_lookup(question: Span, predicate: Union[str, Span], node_type: str, node_value: NounEntity):
    node_span_value = node_value.to_span()

    query_params = [
        f'{ACCESSORS.QUESTION}={question}',
        f'{ACCESSORS.START_I}={predicate.start}',
        f'{ACCESSORS.END_I}={predicate.end}',
        f'{ACCESSORS.TARGET_DATA_TYPE}={DATA_TYPE.SPAN}',
        f'{ACCESSORS.NODE_TYPE}={node_type}',
        f'{ACCESSORS.NODE_VALUE}={node_value.text}',
        f'{ACCESSORS.NODE_START_I}={node_span_value.start}',
        f'{ACCESSORS.NODE_END_I}={node_span_value.end}'
    ]

    matcher_uri = f'http://localhost:8200/{PATHS.MATCHER}?{"&".join(query_params)}'

    return _lookup_formatter(predicate, matcher_uri, node_type, node_value)


def _string_lookup(question: Span, predicate: str, node_type: str, node_value: NounEntity):
    if predicate == "?prop":
        # E.g.: "Give me all ESA astronauts."
        return predicate

    node_span_value = node_value.to_span()

    query_params = [
        f'{ACCESSORS.QUESTION}={question}',
        f'{ACCESSORS.TARGET_EXPRESSION}={predicate}',
        f'{ACCESSORS.TARGET_DATA_TYPE}={DATA_TYPE.STRING}',
        f'{ACCESSORS.NODE_TYPE}={node_type}',
        f'{ACCESSORS.NODE_VALUE}={node_value.text}',
        f'{ACCESSORS.NODE_START_I}={node_span_value.start}',
        f'{ACCESSORS.NODE_END_I}={node_span_value.end}'
    ]

    if predicate not in ["rdf:type"]:
        matcher_uri = f'http://localhost:8200/{PATHS.MATCHER}?{"&".join(query_params)}'
        predicate = text_to_span(predicate)

        return _lookup_formatter(predicate, matcher_uri, node_type, node_value)

    return predicate


def _lookup_formatter(predicate: [str, Span], matcher_uri: str, node_type: str, node_value: NounEntity):
    matcher_response = requests.get(matcher_uri)
    matcher_json = json.loads(matcher_response.content)
    prop_matcher = json.loads(matcher_json['property'])
    prop = RDFProperty(
        prop_matcher["uri"],
        prop_matcher["parent_uris"],
        prop_matcher["label"],
        prop_matcher["ns"],
        prop_matcher["ns_label"],
        prop_matcher["res_domain"],
        prop_matcher["res_range"]
    )
    best_matched = PropertyMatcher(
        prop,
        predicate,
        node_type=node_type,
        node_text_value=node_value.text
    )

    return best_matched
