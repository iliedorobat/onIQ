import re


class Namespace:
    def __init__(self, uri):
        self.name = get_ns_name(uri)
        self.label = get_ns_label(self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            # only equality tests to other 'Namespace' instances are supported
            return NotImplemented
        return self.name == other.name


def get_ns_label(ns_name):
    if ns_name == "http://www.openarchives.org/ore/terms/":
        return "ore"
    elif ns_name == "http://opendata.cs.pub.ro/property/":
        return "opendata"
    elif ns_name == "http://proton.semanticweb.org/protonsys#":
        return "protonsys"
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
        return "owl"
    elif ns_name == "http://www.w3.org/2004/02/skos/core#":
        return "skos"
    elif ns_name == "http://xmlns.com/foaf/0.1/":
        return "foaf"
    else:
        http_prefix = "http://"
        ns_chunk = ns_name[len(http_prefix):]
        return re.sub("[^0-9a-zA-z]", "_", ns_chunk)


def get_ns_name(uri):
    """
    Get the namespace (the namespace is placed before the first '#' character or the last '/' character)
    """
    hash_index = uri.find("#")
    index = hash_index if hash_index != -1 else uri.rfind("/")
    namespace = uri[0: index + 1]
    return namespace
