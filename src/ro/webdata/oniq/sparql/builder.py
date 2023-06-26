import json
from typing import List

import pydash
import requests

from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_ENDPOINT
from ro.webdata.oniq.endpoint.models.RDFElement import URI_TYPE
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.endpoint.query import QueryService, escape_resource_name
from ro.webdata.oniq.service.query_const import ACCESSORS, PATHS
from ro.webdata.oniq.sparql.builder_raw import SPARQLRawBuilder
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion
from ro.webdata.oniq.sparql.model.final_triples.RDFTypeTriple import RDFTypeTriple
from ro.webdata.oniq.sparql.model.final_triples.Triple import Triple
from ro.webdata.oniq.sparql.model.raw_triples.builder_raw_utils import get_improved_raw_triples
from ro.webdata.oniq.sparql.model.raw_triples.raw_target_utils import RawTargetUtils
from ro.webdata.oniq.sparql.model.triples.OrderByRawTriple import OrderByRawTriple
from ro.webdata.oniq.sparql.model.triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.quey import SPARQLQuery


class SPARQLBuilder:
    def __init__(self, endpoint, input_question, print_deps):
        raw_builder = SPARQLRawBuilder(endpoint, input_question, print_deps)
        raw_triples = _prepare_raw_triples(raw_builder)
        raw_triples = get_improved_raw_triples(raw_triples, raw_builder.nl_question)

        self.nl_question = raw_builder.nl_question
        self.targets = _prepare_target_nouns(self.nl_question, raw_triples)
        self.triples = _prepare_triples(raw_triples)

    def to_sparql_query(self):
        return SPARQLQuery.get_query(self.nl_question, self.targets, self.triples)



def _prepare_raw_triples(raw_builder: SPARQLRawBuilder):
    rdf_types = RDFTypeTriple.generate_rdf_types(raw_builder.nl_question.question, raw_builder.raw_triples)
    raw_triples = raw_builder.raw_triples + rdf_types

    order_by_triples = OrderByRawTriple.prepare_extra_raw_triples(raw_builder.nl_question, raw_builder.raw_triples)
    # Exclude the triples used in the ORDER BY statement.
    # Using "set" will change the order or elements.
    # E.g.: "Which museum in New York has the most visitors?"
    main_triples = [raw_triple for raw_triple in raw_triples if raw_triple not in order_by_triples]

    return main_triples + order_by_triples


def _prepare_target_nouns(nl_question: NLQuestion, raw_triples: List[RawTriple]):
    targets = []

    for raw_triple in raw_triples:
        RawTargetUtils.update_targets(nl_question, targets, raw_triple)

    return list(set(targets))


def _prepare_triples(raw_triples: List[RawTriple]):
    if len(raw_triples) == 0:
        return []

    main_raw_triples = [
        raw_triple for raw_triple in raw_triples
        if not raw_triple.is_ordering_triple()
    ]
    order_by_raw_triples = [
        raw_triple for raw_triple in raw_triples
        if raw_triple.is_ordering_triple()
    ]
    rdf_type_order_by_triples = [
        Triple(raw_triple, RDFElements([])) for raw_triple in raw_triples
        # E.g.: "Which musician wrote the most books?"
        if raw_triple.is_rdf_type()
            and raw_triple not in main_raw_triples
            and raw_triple.o.is_dbpedia_type
    ]

    subject = escape_resource_name(
        raw_triples[0].s.to_var()
    )

    main_triples = _init_triples(main_raw_triples, RDFElements([]))
    properties = _get_properties(DBP_ENDPOINT, subject, main_triples + rdf_type_order_by_triples)
    order_by_triples = _init_triples(order_by_raw_triples, properties)

    return main_triples + order_by_triples


def _init_triples(raw_triples: List[RawTriple], properties: RDFElements):
    triples = []

    for raw_triple in raw_triples:
        triple = Triple(raw_triple, properties)
        triples.append(triple)

    return triples


def _get_resource_type(main_triples: List[Triple]):
    rdf_types = [
        triple.o for triple in main_triples
        if isinstance(triple.p, str) and triple.p == "rdf:type"
    ]
    raw_rdf_type = pydash.get(rdf_types, ["0", "text"])

    if raw_rdf_type is None:
        return None

    resource_type_uri = f'http://localhost:8200/{PATHS.RESOURCE_TYPE}?{ACCESSORS.RESOURCE_NAME}={raw_rdf_type}'
    resource_type_response = requests.get(resource_type_uri)
    resource_type: str = json.loads(resource_type_response.content)

    return resource_type


def _get_properties(endpoint: str, subject: str, main_triples: List[Triple]):
    properties = _run_properties_query(endpoint, subject, main_triples)
    resource_type = _get_resource_type(main_triples)

    if resource_type == URI_TYPE.NATURAL_PLACE:
        # Exclude dbo:highest property if the queried resource is a Natural Place.
        # E.g.: What is the highest mountain in Italy?
        #       - dbo:highest will break the result because it doesn't point to
        #           the elevation of the resource, but to the highest mountain of
        #           a mountain range
        return properties.filter(f"{NAMESPACE.DBP_ONTOLOGY}highest")

    return properties


def _run_properties_query(endpoint: str, subject: str, triples: List[Triple]):
    if subject.startswith("?") and len(triples) == 0:
        # E.g.: "Who is the youngest Pulitzer Prize winner?"
        # => subject.startswith("?")
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

    for index, triple in enumerate(triples):
        sparql_query += f"\t\t{triple.to_escaped_str()} ."

        if index < len(triples) - 1:
            sparql_query += "\n"

    sparql_query += f"""
        {subject}   ?property   ?value .
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


def _get_entities(question: str):
    entities_uri = f'http://localhost:8200/{PATHS.ENTITIES}?{ACCESSORS.QUESTION}={question}'
    entities_response = requests.get(entities_uri)
    return json.loads(entities_response.content)
