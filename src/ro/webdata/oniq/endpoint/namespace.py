import re

HTTP_PREFIX = "http://"
NAMESPACE_SEPARATOR = ":"


class NAMESPACE:
    """
    Namespaces.
    """

    DBP_CATEGORY = "http://dbpedia.org/resource/Category:"
    # DBP_ONTOLOGY documentation: https://www.dbpedia.org/resources/ontology/
    DBP_ONTOLOGY = "http://dbpedia.org/ontology/"
    DBP_PROPERTY = "http://dbpedia.org/property/"
    DBP_PAGE = "http://dbpedia.org/page/"
    DBP_RESOURCE = "http://dbpedia.org/resource/"
    DC = "http://purl.org/dc/elements/1.1/"
    DC_TERMS = "http://purl.org/dc/terms/"
    EDM = "http://www.europeana.eu/schemas/edm/"
    FOAF = "http://xmlns.com/foaf/0.1/"
    OPEN_DATA_P = "http://opendata.cs.pub.ro/property/"
    OPEN_DATA_R = "http://opendata.cs.pub.ro/resource/"
    ORE = "http://www.openarchives.org/ore/terms/"
    OWL = "http://www.w3.org/2002/07/owl#"
    PROTONSYS = "http://proton.semanticweb.org/protonsys#"
    PROV = "http://www.w3.org/ns/prov#"
    RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    RDFS = "http://www.w3.org/2000/01/rdf-schema#"
    SKOS = "http://www.w3.org/2004/02/skos/core#"


class NamespaceService:
    """
    Methods:
        get_ns_label(uri):
            Map the namespace to the appropriate label.
        get_namespace(uri):
            Extract the namespace from the target URI.
    """

    @staticmethod
    def get_ns_label(namespace):
        """
        Map the namespace to the appropriate label.

        Args:
            namespace (str): The target URI.

        Returns:
             str: Namespace label.
        """

        if namespace == NAMESPACE.DBP_CATEGORY:
            return "dbcateg"
        elif namespace == NAMESPACE.DBP_ONTOLOGY:
            return "dbo"
        elif namespace == NAMESPACE.DBP_PAGE:
            return "dbpage"
        elif namespace == NAMESPACE.DBP_PROPERTY:
            return "dbp"
        elif namespace == NAMESPACE.DBP_RESOURCE:
            return "dbr"
        elif namespace == NAMESPACE.ORE:
            return "ore"
        elif namespace == NAMESPACE.OPEN_DATA_P:
            return "odp"
        elif namespace == NAMESPACE.PROTONSYS:
            return "protonsys"
        elif namespace == NAMESPACE.PROV:
            return "prov"
        elif namespace == NAMESPACE.DC:
            return "dc"
        elif namespace == NAMESPACE.DC_TERMS:
            return "dcterms"
        elif namespace == NAMESPACE.EDM:
            return "edm"
        elif namespace == NAMESPACE.RDF:
            return "rdf"
        elif namespace == NAMESPACE.RDFS:
            return "rdfs"
        elif namespace == NAMESPACE.OWL:
            return "owl"
        elif namespace == NAMESPACE.SKOS:
            return "skos"
        elif namespace == NAMESPACE.FOAF:
            return "foaf"
        elif namespace == "undefined":
            return namespace
        else:
            ns_chunk = namespace[len(HTTP_PREFIX):]
            return re.sub("[^0-9a-zA-z]", "_", ns_chunk)

    @staticmethod
    def get_namespace(uri):
        """
        Extract the URI placed before the first "#" character or the last
        "/" character.

        Args:
            uri (str): The target URI.

        Returns:
            str: Namespace.
        """

        hash_index = uri.find("#")
        index = hash_index if hash_index != -1 else uri.rfind("/")
        namespace = uri[0: index + 1]

        return namespace
