from typing import Union, List

import spacy
from spacy.tokens import Span

from ro.webdata.oniq.common.nlp.nlp_utils import text_to_span
from ro.webdata.oniq.common.nlp.utils import get_resource_name, get_resource_namespace
from ro.webdata.oniq.endpoint.common.match.PropertiesMatcher import PropertiesMatcher
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_ENDPOINT
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.endpoint.namespace import NAMESPACE, NamespaceService
from ro.webdata.oniq.endpoint.query import QueryService, escape_resource_name
from ro.webdata.oniq.sparql.NounEntity import NounEntity
from ro.webdata.oniq.sparql.triples.raw_triples.RawTriple import RawTriple

nlp_dbpedia = spacy.load('en_core_web_md')
nlp_dbpedia.add_pipe('dbpedia_spotlight', config={'confidence': 0.75})


class SpotlightService:
    @staticmethod
    def adj_property_lookup(predicate: Union[str, Span], props: RDFElements):
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

    @staticmethod
    def property_lookup(question: Span, predicate: Union[str, Span], node_type: str, node_value: NounEntity, raw_triples: List[RawTriple]):
        if isinstance(predicate, str):
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

        new_predicate = predicate
        if str(predicate).lower() == "dissolve":
            # TODO: update PropertiesMatcher.get_best_matched to accept an array of target_expression
            # Use a proper synonym for the word "dissolve"
            # E.g.: "When did the Ming dynasty dissolve?"
            new_predicate = text_to_span("end")

        props = _get_props(raw_triples, new_predicate)
        resource = _extract_dbpedia_resource(question, node_value)

        return PropertiesMatcher.get_best_matched(
            props=props,
            target_expression=new_predicate,
            result_type=None,
            node_type=node_type,
            node_text_value=resource["res_name"]
        )


def _get_props(raw_triples: List[RawTriple], predicate: Union[str, Span]):
    endpoint = DBP_ENDPOINT

    temp_triples = [t for t in raw_triples if str(t.p) == str(predicate)]
    filtered_t = [
        t for t in raw_triples
        if len(temp_triples) == 0
           # E.g.: "How many companies were founded by the founder of Facebook?"
           or t.s == temp_triples[0].s
           # E.g.: "Did Arnold Schwarzenegger attend a university?"
           or t.s == temp_triples[0].o
    ]

    # TODO: return all props if filtered_t contains only a single triple
    #  whose both subject and object are variables
    #  E.g.: "Which musician wrote the most books?"
    return _run_properties_query(endpoint, filtered_t)


def _extract_dbpedia_resource(question: Span, node_value: NounEntity):
    named_entity = _extract_named_entity(question, node_value)

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

            return {
                "res_ns": res_ns,
                "res_ns_label": res_ns_label,
                "res_name": res_name,
                "resource": resource
            }

    return {
        "res_ns": None,
        "res_ns_label": None,
        "res_name": None,
        "resource": None
    }


def _extract_named_entity(question: Span, node_value: NounEntity):
    dbpedia_doc = nlp_dbpedia(question.text)
    ents = dbpedia_doc.ents

    if len(ents) > 0:
        for ent in ents:
            if ent.text == node_value.text:
                return ent

    return node_value.to_span()


def _run_properties_query(endpoint: str, triples: List[RawTriple]):
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
