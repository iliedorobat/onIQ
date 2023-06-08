import json
from typing import List

import pydash
import requests

from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_ENDPOINT
from ro.webdata.oniq.endpoint.models.RDFElement import URI_TYPE
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.endpoint.query import QueryService
from ro.webdata.oniq.service.query_const import ACCESSORS, PATHS
from ro.webdata.oniq.sparql.builder_raw import SPARQLRawBuilder
from ro.webdata.oniq.sparql.model.final_triples.Triple import Triple
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.query import SPARQLQuery


class SPARQLBuilder:
    def __init__(self, endpoint, input_question, print_deps):
        raw_builder = SPARQLRawBuilder(endpoint, input_question, print_deps)

        self.nl_question = raw_builder.nl_question
        self.targets = raw_builder.targets
        self.main_triples = _init_triples(raw_builder.main_triples, RDFElements([]))
        properties = _get_properties(DBP_ENDPOINT, self.main_triples)
        self.order_by_triples = _init_triples(raw_builder.order_by_triples, properties)

    def to_sparql_query(self):
        query = SPARQLQuery(self.nl_question, self.targets, self.main_triples, self.order_by_triples)
        return query.generate_query()


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


def _get_properties(endpoint: str, main_triples: List[Triple]):
    # Exclude dbo:highest property if the queried resource is a Natural Place.
    # E.g.: What is the highest mountain in Italy?
    #       - dbo:highest will break the result because it doesn't point to
    #           the elevation of the resource, but to the highest mountain of
    #           a mountain range

    properties = _run_properties_query(endpoint, main_triples)
    resource_type = _get_resource_type(main_triples)

    if resource_type == URI_TYPE.NATURAL_PLACE:
        return properties.filter(f"{NAMESPACE.DBP_ONTOLOGY}highest")

    return properties


def _run_properties_query(endpoint: str, triples: List[Triple]):
    if len(triples) == 0:
        return RDFElements([])

    first_triple = triples[0]
    subject = first_triple.s.to_var()

    sparql_query = f"""
    PREFIX dbo: <{NAMESPACE.DBP_ONTOLOGY}>
    PREFIX dbr: <{NAMESPACE.DBP_RESOURCE}>
    PREFIX rdf: <{NAMESPACE.RDF}>
    PREFIX rdfs: <{NAMESPACE.RDFS}>

    SELECT DISTINCT ?property ?label ?subclassOf ?domain ?range
    WHERE {{
"""

    for index, triple in enumerate(triples):
        sparql_query += f"\t\t{str(triple)} ."

        if index < len(triples) - 1:
            sparql_query += "\n"

    sparql_query += f"""
        {subject}   ?property   ?value .
        ?property   rdf:type   ?subclassOf .
        ?property   rdfs:label   ?label .
        ?property rdfs:domain ?domain .
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
