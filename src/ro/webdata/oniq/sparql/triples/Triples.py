import json
from typing import List, Union

import pydash
import requests

from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_ENDPOINT
from ro.webdata.oniq.endpoint.models.RDFElement import URI_TYPE
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.endpoint.query import escape_resource_name, QueryService
from ro.webdata.oniq.service.query_const import PATHS, ACCESSORS
from ro.webdata.oniq.sparql.triples.Triple import Triple
from ro.webdata.oniq.sparql.triples.raw_triples.RawTriple import RawTriple


class Triples:
    def __init__(self, raw_triples_values: List[RawTriple]):
        self.values = init_triples(raw_triples_values)


def init_triples(raw_triples_values: List[RawTriple]):
    if len(raw_triples_values) == 0:
        return []

    subject = escape_resource_name(
        raw_triples_values[0].s.to_var()
    )
    properties = _get_properties(DBP_ENDPOINT, subject, raw_triples_values)

    main_raw_triples = [
        raw_triple for raw_triple in raw_triples_values
        if not raw_triple.is_ordering_triple()
    ]
    main_triples = _init_triples(main_raw_triples, properties)

    main_raw_triples = [
        RawTriple(
            s=triple.s,
            p=triple.p,
            o=triple.o,
            question=triple.question
        ) for triple in main_triples
    ]
    order_by_raw_triples = [
        raw_triple for raw_triple in raw_triples_values
        if raw_triple.is_ordering_triple()
    ]

    return _init_triples(main_raw_triples + order_by_raw_triples, properties)


# TODO: main_triples: List[RawTriple]
def _get_properties(endpoint: str, subject: str, main_triples: List[Union[Triple, RawTriple]]):
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


def _init_triples(raw_triples_values: List[RawTriple], properties: RDFElements):
    triples = []

    for raw_triple in raw_triples_values:
        triple = Triple(raw_triple, raw_triples_values, properties)
        triples.append(triple)

    return triples


def _run_properties_query(endpoint: str, subject: str, triples_values: List[Union[Triple, RawTriple]]):
    if subject.startswith("?") and len(triples_values) == 0:
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

    for index, triple in enumerate(triples_values):
        triple_str = triple.to_escaped_str()
        if triple_str is not None:
            sparql_query += f"\t\t{triple.to_escaped_str()} ."

        if index < len(triples_values) - 1:
            sparql_query += "\n"

    if not subject.startswith("?"):
        # E.g.: "How many companies were founded by the founder of Facebook?"
        # => subject.startswith("?")
        sparql_query += f"\t\t{subject}   ?property   ?value ."

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
