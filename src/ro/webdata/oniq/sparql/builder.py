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
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, QUESTION_TYPES
from ro.webdata.oniq.sparql.model.raw_triples.builder_raw_utils import get_improved_raw_triples
from ro.webdata.oniq.sparql.model.final_triples.Triple import Triple
from ro.webdata.oniq.sparql.model.raw_triples.raw_target_utils import RawTargetUtils
from ro.webdata.oniq.sparql.model.triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.model.triples.OrderByRawTriple import OrderByRawTriple
from ro.webdata.oniq.sparql.model.final_triples.RDFTypeTriple import RDFTypeTriple


class QUERY_TYPES:
    ASK = "ASK"
    COUNT = "COUNT"
    SELECT = "SELECT"


class SPARQLBuilder:
    def __init__(self, endpoint, input_question, print_deps):
        raw_builder = SPARQLRawBuilder(endpoint, input_question, print_deps)
        raw_triples = _prepare_raw_triples(raw_builder)
        raw_triples = get_improved_raw_triples(raw_triples, raw_builder.nl_question)

        self.nl_question = raw_builder.nl_question
        self.targets = _prepare_target_nouns(self.nl_question, raw_triples)
        self.triples = _prepare_triples(raw_triples)

    def to_sparql_query(self):
        query_type = _get_query_type(self.nl_question)
        output = ""

        if query_type == QUERY_TYPES.ASK:
            output = "ASK"
        else:
            str_targets = [target.to_var() for target in self.targets]
            output = f"SELECT DISTINCT {' '.join(str_targets)}"

        str_triples = [f"\t{str(triple)}" for triple in self.triples]
        output += "\n"
        output += "WHERE {\n"
        output += " .\n".join(str_triples) + "\n"
        output += "}"

        str_ordering_triples = list(
            set([
                f"{str(item.order_by)}"
                for item in self.triples
                if item.is_ordering_triple()
            ])
        )

        if len(str_ordering_triples) > 0:
            output += "\n"
            output += f"ORDER BY {' '.join(str_ordering_triples)}"

        return output


def _get_query_type(nl_question):
    if nl_question.question_type == QUESTION_TYPES.S_AUX:
        return QUERY_TYPES.ASK
    elif nl_question.question_type == QUESTION_TYPES.COUNT:
        return QUERY_TYPES.COUNT

    return QUERY_TYPES.SELECT


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
    target_nouns = []

    for raw_triple in raw_triples:
        RawTargetUtils.update_target_nouns(nl_question, target_nouns, raw_triple)

    return list(set(target_nouns))


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

    if not subject.startswith("?"):
        sparql_query += f"{subject}   ?property   ?value ."

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


def _get_entities(question: str):
    entities_uri = f'http://localhost:8200/{PATHS.ENTITIES}?{ACCESSORS.QUESTION}={question}'
    entities_response = requests.get(entities_uri)
    return json.loads(entities_response.content)
