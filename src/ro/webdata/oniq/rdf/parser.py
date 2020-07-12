# https://rdflib.dev/sparqlwrapper/
from SPARQLWrapper import SPARQLWrapper, JSON
from pathlib import Path
from rdflib import Graph, Literal

from ro.webdata.oniq.rdf.namespace.Namespace import Namespace
from ro.webdata.oniq.rdf.property.Property import Property

CLASSES_QUERY = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT DISTINCT ?uri
    WHERE {
        ?s rdf:type ?uri .
        FILTER(?uri != rdf:Property)
    }
    ORDER BY ?uri
"""

PROPERTIES_QUERY = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?uri
    WHERE {
        ?uri rdf:type ?o .
        FILTER(
            ?uri NOT IN (rdf:type, rdfs:subPropertyOf, rdfs:subClassOf) &&
            ?o = rdf:Property
        )
    }
    ORDER BY ?uri
"""


def get_namespaces(endpoint):
    """
    Get the list of namespaces
    """

    nss = []
    uris = _get_uris(endpoint, CLASSES_QUERY) + _get_uris(endpoint, PROPERTIES_QUERY)

    for uri in uris:
        nss.append(Namespace(uri))

    return list(set(nss))


def get_properties(endpoint):
    """
    Get the list of properties
    """

    props = []
    uris = _get_uris(endpoint, PROPERTIES_QUERY)

    for uri in uris:
        prop = Property(uri)
        if prop.__bool__():
            props.append(prop)

    return props


def _get_uris(endpoint, query):
    """
    Get the list of URIs
    """

    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    output = sparql.query().convert()

    uris = set()
    for result in output["results"]["bindings"]:
        uri = result["uri"]["value"]
        uris.add(uri)

    return sorted(uris)


# TODO: add some additional params (path, file_name, extension, format)
def parse_rdf(file_name):
    graph = Graph()
    graph.parse(file_name)

    for s, p, o in graph:
        if isinstance(o, Literal):
            graph.add([s, p, Literal("tt", o.language)])
            graph.remove([s, p, o])

    path = str(Path.home()) + "/workspace/personal/semIQ/files/output"
    graph.serialize(destination=path + "/test.rdf", format="turtle")
