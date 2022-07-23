from typing import List

import pydash
import requests
from spacy.tokens import Span, Token

from ro.webdata.oniq.common.text_utils import WORD_SEPARATOR
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertiesMatcher
from ro.webdata.oniq.endpoint.common.translator.CSVTranslator import CSVTranslator
from ro.webdata.oniq.endpoint.common.translator.URITranslator import URITranslator
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_PROPERTIES_OF_RESOURCE_QUERY
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_RESOURCE_QUERY, DBP_ONTOLOGY_RESOURCE_QUERY
from ro.webdata.oniq.endpoint.models.RDFElement import RDFClass, ROOT_CLASS_URI

_MAX_LOOKUP_RESULTS = 10
_NAME_TYPE_SEPARATOR = ','
# DBpedia lookup API documentation:
#       https://www.dbpedia.org/resources/lookup/
#       https://github.com/dbpedia/dbpedia-lookup
_DBP_LOOKUP_API = "https://lookup.dbpedia.org/api/search"


class LookupService:
    """
    Methods:
        entities_lookup(named_entity, output_format="JSON"):
            Retrieve the list of DBpedia classes which best match the target
            named entity.
        noun_chunk_lookup(noun_chunk, output_format="JSON"):
            Retrieve the list of DBpedia classes which best match the target
            noun chunk.
        property_lookup(resource_name, verb):
            Lookup for the property which has the highest similarity degree
            with the verb.
    """

    @staticmethod
    def entities_lookup(named_entity, output_format="JSON"):
        """
        Retrieve the list of DBpedia classes which best match the target
        named entity.

        E.g.:
            - named_entity: "Will Smith" (original query: "Who is Will Smith?").
            - named_entity: "James Cagney" (original query: "What did James Cagney
                win in the 15th Academy Awards?").

        Args:
            named_entity (Span): Named entity (E.g.: "James Cagney").
            output_format (str): XML or JSON.

        Returns:
            List[dict]: List of dictionaries describing DBpedia classes best match
                the target named entity.
        """

        types = _get_named_entity_types(named_entity)
        params = _generate_lookup_params(types, output_format, named_entity)
        response = requests.get(_DBP_LOOKUP_API, params)

        return response.json().get("docs")

    @staticmethod
    def noun_chunk_lookup(noun_chunk, output_format="JSON"):
        """
        Retrieve the list of DBpedia classes which best match the target
        noun chunk.

        E.g.:
            - noun_chunk: "rizal monument" (original query: "What is rizal
                monument all about?")

        Args:
            noun_chunk (Span): Noun chunk (E.g. "rizal monument").
            output_format (str): XML or JSON.

        Returns:
            List[dict]: List of dictionaries describing DBpedia classes best match
                the target noun chunk.
        """

        types = _get_noun_chunk_types(noun_chunk)
        params = _generate_lookup_params(types, output_format, noun_chunk)
        response = requests.get(_DBP_LOOKUP_API, params)

        return response.json().get("docs")

    @staticmethod
    def property_lookup(resource_name, action):
        """
        Lookup for the property which has the highest similarity degree with the verb.

        Args:
            resource_name (str): Name of the resource (E.g.: "Barda_Mausoleum").
            action (Token): Target verb used for looking up for a property.

        Returns:
             RDFProperty: Property having the highest similarity degree with the verb.
        """

        sparql_query = DBP_PROPERTIES_OF_RESOURCE_QUERY % resource_name
        props = DBpediaQueryService.run_properties_query(sparql_query)

        matcher = PropertiesMatcher(props, action)
        best_matched = matcher.get_best_matched()

        return pydash.get(best_matched, "property")

    @staticmethod
    def resource_lookup(resource_name):
        """
        Lookup for a specific resource.

        Args:
            resource_name (str): Resource name.

        Returns:
            RDFClass: Identified resource.
        """

        resource_type = DBpediaQueryService.run_resource_query(resource_name, DBP_ONTOLOGY_RESOURCE_QUERY)

        if resource_type is None:
            resource_type = DBpediaQueryService.run_resource_query(resource_name, DBP_RESOURCE_QUERY)

        return resource_type


def _generate_lookup_params(types, output_format, noun_chunk):
    """
    Generate the dictionary to send in the query string for the :class:`Request`.

    Args:
        types (List[RDFClass]): List of parent classes.
        output_format (str): XML or JSON.
        noun_chunk (Span): Noun chunk (E.g. "rizal monument").

    Returns:
         dict: Query params.
    """

    params = {
        "format": output_format,
        "query": noun_chunk.text,
        "maxResults": _MAX_LOOKUP_RESULTS
    }

    if len(types) > 0:
        names = [item.name for item in types]
        params["typeName"] = _NAME_TYPE_SEPARATOR.join(names)

    return params


def _get_noun_chunk_types(noun_chunk):
    """
    Retrieve the list of parent classes of the noun_chunk.

    Args:
        noun_chunk (Span): Noun chunk (E.g. "rizal monument").

    Returns:
        List[RDFClass]
    """

    types = []

    # E.g.: "when was barda mausoleum built?"
    #   => resource_name: "Barda_Mausoleum"
    resource_name = noun_chunk.text.title().replace(WORD_SEPARATOR, "_")
    resource = LookupService.resource_lookup(resource_name)

    if resource is not None:
        resource_types = []

        uri_translator = URITranslator()
        for parent_uri in resource.parent_uris:
            if parent_uri != ROOT_CLASS_URI:
                resource_types += uri_translator.to_classes([parent_uri])

        resource_types.reverse()
        types += resource_types

    # E.g.: "when was barda mausoleum built?"
    #   => word: "barda", "mausoleum"
    for word in noun_chunk:
        resource_name = word.text.strip().capitalize()
        resource = LookupService.resource_lookup(resource_name)
    
        if resource is not None:
            types.append(resource)

    return list(set(types))


def _get_named_entity_types(named_entity: Span):
    """
    Retrieve the list of types extracted based on the named_entity.label_.

    E.g.:
        - named_entity: "Will Smith" (original query: "Who is Will Smith?").
        - named_entity: "James Cagney" (original query: "What did James Cagney
            win in the 15th Academy Awards?").

    Args:
        named_entity (Span): Named entity (E.g.: "James Cagney").

    Returns:
         List[RDFClass]: List of types.
    """

    classes = CSVTranslator.to_classes()
    label = named_entity.label_

    if label == "DATE" or label == "TIME":
        return [item for item in classes if item.uri == "http://dbpedia.org/ontology/TimePeriod"]
    elif label == "EVENT":
        return [item for item in classes if item.uri == "http://dbpedia.org/ontology/Event"]
    elif label == "FAC":
        # FAC Buildings, airports, highways, bridges, etc
        return [item for item in classes if item.uri == "http://dbpedia.org/ontology/Building"]
    elif label == "GPE" or label == "LOC":
        # GPE Countries, cities, states
        # LOC Non-GPE locations, mountain ranges, bodies of water
        return [item for item in classes if item.uri == "http://dbpedia.org/ontology/Place"]
    elif label == "LANGUAGE":
        return [item for item in classes if item.uri == "http://dbpedia.org/ontology/Language"]
    elif label == "LAW":
        return [item for item in classes if item.uri == "http://dbpedia.org/ontology/Law"]
    elif label == "MONEY":
        return [item for item in classes if item.uri == "http://dbpedia.org/ontology/Currency"]
    elif label == "NORP":
        # Nationalities or religious or political groups
        return [
            item for item in classes if item.uri in [
                "http://dbpedia.org/ontology/EthnicGroup",
                "http://dbpedia.org/ontology/PoliticalParty",
                "http://dbpedia.org/ontology/ReligiousOrganisation"
            ]
        ]
    elif label == "ORG":
        return [item for item in classes if item.uri == "http://dbpedia.org/ontology/Organisation"]
    elif label == "PERSON":
        return [item for item in classes if item.uri == "http://dbpedia.org/ontology/Person"]
    elif label == "PRODUCT":
        # Objects, vehicles, foods, etc. (Not services)
        return [
            item for item in classes if item.uri in [
                "http://dbpedia.org/ontology/ArchitecturalStructure",
                "http://dbpedia.org/ontology/CelestialBody",
                "http://dbpedia.org/ontology/ChemicalSubstance",
                "http://dbpedia.org/ontology/Device",
                "http://dbpedia.org/ontology/Engine",
                "http://dbpedia.org/ontology/Flag",
                "http://dbpedia.org/ontology/Food",
                "http://dbpedia.org/ontology/MeanOfTransportation",
                "http://dbpedia.org/ontology/Satellite",
                "http://dbpedia.org/ontology/WrittenWork",

                "http://dbpedia.org/ontology/Album",
                "http://dbpedia.org/ontology/Award",
                "http://dbpedia.org/ontology/UnitOfWork",
                "http://dbpedia.org/ontology/Software",
                "http://dbpedia.org/ontology/Spreadsheet",
                "http://dbpedia.org/ontology/Website"
            ]
        ]
    elif label == "QUANTITY":
        return [
            item for item in classes if item.uri in [
                "http://dbpedia.org/ontology/Altitude",
                "http://dbpedia.org/ontology/Depth",
                "http://dbpedia.org/ontology/GrossDomesticProduct",
                "http://dbpedia.org/ontology/GrossDomesticProductPerCapita"
            ]
        ]
    elif label == "WORK_OF_ART":
        return [item for item in classes if item.uri == "http://dbpedia.org/ontology/Artwork"]

    return []
