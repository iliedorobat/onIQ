import json
from typing import Union

import requests
from spacy.tokens import Span

from ro.webdata.oniq.common.nlp.nlp_utils import text_to_span
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.models.RDFElement import RDFProperty
from ro.webdata.oniq.service.query_const import PATHS, ACCESSORS, VALUES
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity


def object_predicate_lookup(question: Span, obj: NounEntity, predicate: Span):
    if isinstance(predicate, Span):
        # E.g.: "Who is the youngest Pulitzer Prize winner?"
        #       <?person   winner   dbr:Pulitzer_Prize>
        return _span_lookup(
            question=question,
            predicate=predicate,
            object_uri=obj.to_var()
        )

    elif isinstance(predicate, str):
        # E.g.: "Give me all Swedish holidays."
        #       <?holiday   "country"   dbr:Sweden>
        return _string_lookup(
            question=question,
            predicate=predicate,
            target_object=obj.to_var()
        )

    return predicate


def subject_predicate_lookup(question: Span, subject: NounEntity, predicate: Union[str, Span]):
    if isinstance(predicate, Span):
        # E.g.: "In which country is Mecca located?"
        #       <dbr:Mecca   country   ?country>
        return _span_lookup(
            question=question,
            predicate=predicate,
            subject_uri=subject.to_var()
        )

    return predicate


def _span_lookup(question: Span, predicate: Union[str, Span], subject_uri: str = None, object_uri: str = None):
    query_params = [
        f'{ACCESSORS.QUESTION}={question}',
        f'{ACCESSORS.START_I}={predicate.start}',
        f'{ACCESSORS.END_I}={predicate.end}',
        f'{ACCESSORS.TARGET_TYPE}={VALUES.SPAN}'
    ]
    if object_uri is not None:
        query_params.append(f'{ACCESSORS.TARGET_OBJECT}={object_uri}')
    if subject_uri is not None:
        query_params.append(f'{ACCESSORS.TARGET_SUBJECT}={subject_uri}')

    matcher_uri = f'http://localhost:8200/{PATHS.MATCHER}?{"&".join(query_params)}'

    return _lookup_formatter(
        predicate=predicate,
        matcher_uri=matcher_uri,
        subject_uri=subject_uri,
        object_uri=object_uri
    )


def _string_lookup(question: Span, predicate: Union[str, Span], target_object: str):
    query_params = [
        f'{ACCESSORS.QUESTION}={question}',
        f'{ACCESSORS.TARGET_EXPRESSION}={predicate}',
        f'{ACCESSORS.TARGET_TYPE}={VALUES.STRING}'
    ]
    if target_object is not None:
        query_params.append(f'{ACCESSORS.TARGET_OBJECT}={target_object}')

    if predicate not in ["rdf:type"]:
        matcher_uri = f'http://localhost:8200/{PATHS.MATCHER}?{"&".join(query_params)}'

        return _lookup_formatter(
            predicate=text_to_span(predicate),
            matcher_uri=matcher_uri,
            object_uri=target_object
        )

    return predicate


def _lookup_formatter(predicate: [str, Span], matcher_uri: str, subject_uri: str = None, object_uri: str = None):
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
        subject_uri=subject_uri,
        object_uri=object_uri
    )

    return best_matched
