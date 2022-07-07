import warnings

from rdflib import Graph

from ro.webdata.oniq.model.rdf.Namespace import Namespace
from ro.webdata.oniq.model.rdf.Property import Property
from ro.webdata.oniq.endpoint.query import QueryService
from ro.webdata.oniq.endpoint.sparql_query import CLASSES_QUERY, PROPERTIES_QUERY


def parse_rdf(file_name):
    """
    TODO: parse & query the local RDF file:
        https://stackoverflow.com/questions/9877989/python-sparql-querying-local-file
    TODO: add some additional params (path, file_name, extension, format)
    """

    graph = Graph()
    graph.parse(file_name)

    # for s, p, o in graph:
    #     if isinstance(o, Literal):
    #         print(f'{s} {p} {o}')
    #         graph.add([s, p, Literal("tt", o.language)])
    #         graph.remove([s, p, o])
    # graph.serialize(destination=get_output_file_path("test", "rdf"), format="turtle")

    return graph


def get_namespaces(endpoint):
    """
    Get the list of namespaces
    """

    warnings.warn("deprecated in favour of QueryService.run_classes_query", DeprecationWarning)

    nss = []
    uris = _get_uris(endpoint, CLASSES_QUERY) + _get_uris(endpoint, PROPERTIES_QUERY)

    for uri in uris:
        nss.append(Namespace(uri))

    return list(set(nss))


def get_properties(endpoint):
    """
    Get the list of properties
    """

    warnings.warn("deprecated in favour of QueryService.run_properties_query", DeprecationWarning)

    props = []
    uris = _get_uris(endpoint, PROPERTIES_QUERY)

    for index, uri in enumerate(uris):
        prop = Property(uri)
        if prop.__bool__():
            props.append(prop)

    return props


def _get_uris(endpoint, query):
    """
    Get the list of URIs
    """

    output = QueryService.run_query(endpoint, query)

    uris = set()
    for result in output["results"]["bindings"]:
        uri = result["uri"]["value"]
        uris.add(uri)

    return sorted(uris)
