import json
from typing import Union, List

import requests
import spacy
from spacy.tokens import Span

from ro.webdata.oniq.common.nlp.nlp_utils import text_to_span
from ro.webdata.oniq.common.nlp.utils import get_resource_name, get_resource_namespace
from ro.webdata.oniq.endpoint.common.match.PropertiesMatcher import PropertiesMatcher
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_ENDPOINT
from ro.webdata.oniq.endpoint.models.RDFElement import RDFProperty
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.endpoint.namespace import NAMESPACE, NamespaceService
from ro.webdata.oniq.endpoint.query import QueryService, escape_resource_name
from ro.webdata.oniq.service.query_const import PATHS, ACCESSORS, DATA_TYPE, NODE_TYPE
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.triples.RawTriple import RawTriple

nlp_dbpedia = spacy.load('en_core_web_md')
nlp_dbpedia.add_pipe('dbpedia_spotlight', config={'confidence': 0.75})


def adjective_property_lookup(predicate: Union[str, Span], props: RDFElements):
    if isinstance(predicate, Span):
        best_matched = PropertiesMatcher.get_best_matched(
            props=props,
            target_expression=predicate
        )

        return best_matched

    # E.g.: "Who is the youngest Pulitzer Prize winner?"
    #       <?person   dbo:birthDate   ?youngest>
    # E.g.: "What is the highest mountain in Italy?"
    #       <?mountain   highest   ?highest>
    return predicate


def object_predicate_lookup(question: Span, obj: NounEntity, predicate: Span, raw_triples: List[RawTriple]):
    if isinstance(predicate, Span):
        # E.g.: "Who is the youngest Pulitzer Prize winner?"
        #       <?person   winner   dbr:Pulitzer_Prize>
        return _span_lookup(
            question=question,
            predicate=predicate,
            node_type=NODE_TYPE.OBJECT,
            node_value=obj,
            raw_triples=raw_triples
        )

    elif isinstance(predicate, str):
        # E.g.: "Give me all Swedish holidays."
        #       <?holiday   "country"   dbr:Sweden>

        # E.g.: "Give me all ESA astronauts."
        #       <?astronaut   ?property   dbr:ESA>
        return _string_lookup(
            question=question,
            predicate=predicate,
            node_type=NODE_TYPE.OBJECT,
            node_value=obj
        )

    return predicate


def subject_predicate_lookup(question: Span, subject: NounEntity, predicate: Union[str, Span], raw_triples: List[RawTriple]):
    if isinstance(predicate, Span):
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
            node_value=subject,
            raw_triples=raw_triples
        )

    return predicate


def _span_lookup(question: Span, predicate: Union[str, Span], node_type: str, node_value: NounEntity, raw_triples: List[RawTriple]):
    endpoint = DBP_ENDPOINT
    dbpedia_doc = nlp_dbpedia(question.text)

    ents = dbpedia_doc.ents
    named_entity = node_value.to_span()
    res_name = None
    resource = None
    props = []

    if len(ents) > 0:
        for ent in ents:
            if ent.text == node_value.text:
                named_entity = ent

    if named_entity is not None:
        # E.g. "Which volcanos in Japan erupted since 2000?"
        # => named_entity is None
        if named_entity.label_ == "DBPEDIA_ENT" and named_entity.kb_id_ != "":
            # E.g.: "What is the net income of Apple?"
            # E.g.: "When did the Ming dynasty dissolve?" => named_entity.kb_id_ == ""
            res_ns = get_resource_namespace(named_entity)
            res_ns_label = NamespaceService.get_ns_label(res_ns)
            res_name = get_resource_name(named_entity)
            resource = f"{res_ns_label}:{escape_resource_name(res_name)}"

    temp_triples = [t for t in raw_triples if str(t.p) == str(predicate)]
    filtered_t = [
        t for t in raw_triples
        if len(temp_triples) == 0
        # E.g.: "How many companies were founded by the founder of Facebook?"
           or t.s == temp_triples[0].s
        # E.g.: "Did Arnold Schwarzenegger attend a university?"
           or t.s == temp_triples[0].o
    ]

    if node_type == NODE_TYPE.SUBJECT:
        props = _run_properties_query(endpoint, filtered_t, resource, None)

    if node_type == NODE_TYPE.OBJECT:
        props = _run_properties_query(endpoint, filtered_t, None, resource)

    best_matched = PropertiesMatcher.get_best_matched(
        props=props,
        target_expression=predicate,
        result_type=None,
        node_type=node_type,
        node_text_value=res_name
    )

    return best_matched


def _run_properties_query(endpoint: str, triples: List[RawTriple], subject: Union[str, None], obj: Union[str, None]):
    if len(triples) == 0:
        return RDFElements([])

    sparql_query = f"""
    PREFIX dbo: <{NAMESPACE.DBP_ONTOLOGY}>
    PREFIX dbp: <{NAMESPACE.DBP_PROPERTY}>
    PREFIX dbr: <{NAMESPACE.DBP_RESOURCE}>
    PREFIX rdf: <{NAMESPACE.RDF}>
    PREFIX rdfs: <{NAMESPACE.RDFS}>

    SELECT DISTINCT ?property ?label ?subclassOf ?domain ?range
    WHERE {{
"""

    for triple in triples:
        triple_str = triple.to_escaped_str()
        if triple_str is not None:
            sparql_query += f"\t\t{triple_str} .\n"

    sparql_query += f"""
        ?property   rdf:type   ?subclassOf .
        ?property   rdfs:label   ?label .
        OPTIONAL {{ ?property   rdfs:domain   ?domain }} .
        OPTIONAL {{ ?property rdfs:range ?range }} .
        FILTER(
            ?property NOT IN (rdf:type, rdfs:subPropertyOf, rdfs:subClassOf) &&
            ?subclassOf = rdf:Property
        )
        FILTER(langMatches(lang(?label), "en"))
    }}
    ORDER BY ?property
"""

    return QueryService.run_properties_query(endpoint, sparql_query)


def _string_lookup(question: Span, predicate: str, node_type: str, node_value: NounEntity):
    if predicate == "?property":
        # E.g.: "Give me all ESA astronauts."
        return predicate

    if predicate.startswith("dbo:"):
        # E.g.: "What is the highest mountain in Italy?"
        return predicate

    if predicate.startswith("rdf:"):
        # E.g.: "Who is the tallest basketball player?"
        return predicate

    if predicate == "country":
        # E.g.: "Give me all Swedish holidays."
        return "dbo:country"

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
    matcher_uri = f'http://localhost:8200/{PATHS.MATCHER}?{"&".join(query_params)}'
    predicate = text_to_span(predicate)

    return _lookup_formatter(predicate, matcher_uri, node_type, node_value)


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
