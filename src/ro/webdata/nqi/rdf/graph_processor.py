from pathlib import Path
import re

# https://rdflib.dev/sparqlwrapper/
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal
from iteration_utilities import unique_everseen

from ro.webdata.nqi.common.text_utils import split_camel_case_string

PROPERTIES_QUERY = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?name
    WHERE {
        ?name ?p ?o .
        FILTER(
            ?name NOT IN (rdf:type, rdfs:subPropertyOf, rdfs:subClassOf) &&
            ?p = rdf:type &&
            ?o = rdf:Property
        )
    }
    ORDER BY ?name
"""


# TODO: rename to something more generic
def generate_properties_map(endpoint):
    properties_map = []
    rdf_properties = get_classes(endpoint)

    for rdf_property in rdf_properties:
        ns_name = get_ns_name(rdf_property)
        ns_label = get_ns_label(ns_name)
        prop_name = get_property_name(rdf_property)

        # TODO: check for http://www.w3.org/1999/02/22-rdf-syntax-ns#_1 in the triple
        if prop_name != "_1":
            properties_map.append({
                "ns_label": ns_label,
                "ns_name": ns_name,
                "prop_label": split_camel_case_string(prop_name),
                "prop_name": prop_name,
                "prop_name_extended": ns_label + "_" + prop_name,
                "short_name": ns_label + ":" + prop_name
            })

    return properties_map


# TODO: rename the param with something more generic
def generate_namespaces_map(properties_map):
    mapped_list = list(
        map(
            lambda item: {
                "ns_label": item["ns_label"],
                "ns_name": item["ns_name"]
            }, properties_map
        )
    )

    return list(unique_everseen(mapped_list))


def get_classes(endpoint, query=PROPERTIES_QUERY):
    """
    Get the list of properties (namespace + property name)
    """
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    output = sparql.query().convert()

    rdf_classes = set()
    for result in output["results"]["bindings"]:
        value = result["name"]["value"]
        rdf_classes.add(value)

    return sorted(rdf_classes)


def get_property_name(uri):
    """
    Remove the namespace and return the name of the property
    """
    namespace = get_ns_name(uri)
    property_name = uri[len(namespace):]

    if property_name == "basediameter":
        return "baseDiameter"
    elif property_name == "conjugatediameter":
        return "conjugateDiameter"
    elif property_name == "handlediameter":
        return "handleDiameter"
    elif property_name == "maximaldiameter":
        return "maximalDiameter"
    elif property_name == "mouthdiameter":
        return "mouthDiameter"
    elif property_name == "sleevewidth":
        return "sleeveWidth"
    elif property_name == "transversediameter":
        return "transverseDiameter"
    else:
        return property_name


def get_ns_name(uri):
    """
    Get the namespace (the namespace is placed before the first '#' character or the last '/' character)
    """
    hash_index = uri.find("#")
    index = hash_index if hash_index != -1 else uri.rfind("/")
    namespace = uri[0: index + 1]
    return namespace


def get_ns_label(ns_name):
    if ns_name == "http://opendata.cs.pub.ro/property/":
        return "opendata"
    elif ns_name == "http://purl.org/dc/elements/1.1/":
        return "dc"
    elif ns_name == "http://purl.org/dc/terms/":
        return "dcterms"
    elif ns_name == "http://www.europeana.eu/schemas/edm/":
        return "edm"
    elif ns_name == "http://www.w3.org/1999/02/22-rdf-syntax-ns#":
        return "rdf"
    elif ns_name == "http://www.w3.org/2000/01/rdf-schema#":
        return "rdfs"
    elif ns_name == "http://www.w3.org/2002/07/owl#":
        return "owl";
    elif ns_name == "http://www.w3.org/2004/02/skos/core#":
        return "skos"
    elif ns_name == "http://xmlns.com/foaf/0.1/":
        return "foaf"
    else:
        http_prefix = "http://"
        ns_chunk = ns_name[len(http_prefix):]
        return re.sub("[^0-9a-zA-z]", "_", ns_chunk)


# TODO: add some additional params (path, file name, extension, format)
def parse_rdf(file_name):
    graph = Graph()
    graph.parse(file_name)

    for s, p, o in graph:
        if isinstance(o, Literal):
            graph.add([s, p, Literal("tt", o.language)])
            graph.remove([s, p, o])

    path = str(Path.home()) + "/workspace/personal/semIQ/files/output"
    graph.serialize(destination=path + "/test.rdf", format="turtle")
