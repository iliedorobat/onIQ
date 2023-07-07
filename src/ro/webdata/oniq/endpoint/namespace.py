import re

from ro.webdata.oniq.common.print_utils import console
from ro.webdata.oniq.sparql.common.constants import SPARQL_STR_SEPARATOR

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
    GEORSS = "http://www.georss.org/georss/"
    LINGUISTICS_GOLD = "http://purl.org/linguistics/gold/"
    OPEN_DATA_P = "http://opendata.cs.pub.ro/property/"
    OPEN_DATA_R = "http://opendata.cs.pub.ro/resource/"
    ORE = "http://www.openarchives.org/ore/terms/"
    OWL = "http://www.w3.org/2002/07/owl#"
    PROTONSYS = "http://proton.semanticweb.org/protonsys#"
    PROV = "http://www.w3.org/ns/prov#"
    RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    RDFS = "http://www.w3.org/2000/01/rdf-schema#"
    SCHEMA_ORG = "http://schema.org/"
    SKOS = "http://www.w3.org/2004/02/skos/core#"
    WGS84 = "http://www.w3.org/2003/01/geo/wgs84_pos#"
    XML_2001 = "http://www.w3.org/2001/XMLSchema#"


class NamespaceService:
    """
    Methods:
        get_ns_label(uri):
            Map the namespace to the appropriate label.
        get_namespace(uri):
            Extract the namespace from the target URI.
    """

    @staticmethod
    def extract_namespace(value: str):
        if value is None:
            return None

        index = value.find(":")
        if index > -1:
            ns_label = value[0: index]
            return NamespaceService.get_ns_uri(ns_label)

        return None

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
        elif namespace == NAMESPACE.GEORSS:
            return "georss"
        elif namespace == NAMESPACE.LINGUISTICS_GOLD:
            return "linguistics"
        elif namespace == NAMESPACE.RDF:
            return "rdf"
        elif namespace == NAMESPACE.RDFS:
            return "rdfs"
        elif namespace == NAMESPACE.OWL:
            return "owl"
        elif namespace == NAMESPACE.SCHEMA_ORG:
            return "schemaOrg"
        elif namespace == NAMESPACE.SKOS:
            return "skos"
        elif namespace == NAMESPACE.FOAF:
            return "foaf"
        elif namespace == NAMESPACE.WGS84:
            return "wgs84"
        elif namespace == "undefined":
            return namespace
        else:
            ns_chunk = namespace[len(HTTP_PREFIX):]
            return re.sub("[^0-9a-zA-z]", SPARQL_STR_SEPARATOR, ns_chunk)

    @staticmethod
    def get_ns_uri(ns_label):
        if ns_label == "dbcateg":
            return NAMESPACE.DBP_CATEGORY
        elif ns_label == "dbo":
            return NAMESPACE.DBP_ONTOLOGY
        elif ns_label == "dbpage":
            return NAMESPACE.DBP_PAGE
        elif ns_label == "dbp":
            return NAMESPACE.DBP_PROPERTY
        elif ns_label == "dbr":
            return NAMESPACE.DBP_RESOURCE
        elif ns_label == "ore":
            return NAMESPACE.ORE
        elif ns_label == "odp":
            return NAMESPACE.OPEN_DATA_P
        elif ns_label == "protonsys":
            return NAMESPACE.PROTONSYS
        elif ns_label == "prov":
            return NAMESPACE.PROV
        elif ns_label == "dc":
            return NAMESPACE.DC
        elif ns_label == "dcterms":
            return NAMESPACE.DC_TERMS
        elif ns_label == "edm":
            return NAMESPACE.EDM
        elif ns_label == "georss":
            return NAMESPACE.GEORSS
        elif ns_label == "linguistics":
            return NAMESPACE.LINGUISTICS_GOLD
        elif ns_label == "rdf":
            return NAMESPACE.RDF
        elif ns_label == "rdfs":
            return NAMESPACE.RDFS
        elif ns_label == "owl":
            return NAMESPACE.OWL
        elif ns_label == "schemaOrg":
            return NAMESPACE.SCHEMA_ORG
        elif ns_label == "skos":
            return NAMESPACE.SKOS
        elif ns_label == "foaf":
            return NAMESPACE.FOAF
        elif ns_label == "wgs84":
            return NAMESPACE.WGS84
        else:
            console.error(f"The label \"{ns_label}\" does not exists!")

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
