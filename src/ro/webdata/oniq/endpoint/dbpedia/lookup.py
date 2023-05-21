import json
from typing import List

import pydash
import requests
from spacy.tokens import Span, Token

from ro.webdata.oniq.common.text_utils import WORD_SEPARATOR
from ro.webdata.oniq.endpoint.common.CSVService import CSVService
from ro.webdata.oniq.endpoint.common.match.PropertiesMatcher import PropertiesMatcher
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.common.path_utils import get_dbpedia_file_path
from ro.webdata.oniq.endpoint.common.translator.CSVTranslator import CSVTranslator
from ro.webdata.oniq.endpoint.common.translator.URITranslator import URITranslator
from ro.webdata.oniq.endpoint.dbpedia.constants import DBPEDIA_CLASS_TYPES
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_PROPERTIES_OF_RESOURCE_QUERY
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_RESOURCE_QUERY, DBP_ONTOLOGY_RESOURCE_QUERY
from ro.webdata.oniq.endpoint.models.RDFElement import RDFClass, RDFProperty, ROOT_CLASS_URI
from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.service.query_const import ACCESSORS, PATHS
from ro.webdata.oniq.sparql.constants import SPARQL_STR_SEPARATOR

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
    def property_lookup(resource_name, action, result_type):
        """
        Lookup for the property which has the highest similarity degree with the verb.

        Args:
            resource_name (str):
                Name of the resource (E.g.: "Barda_Mausoleum").
            action (Token):
                Target word used for looking up for a property.
            result_type (str|None):
                Type of the expected result.
                E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).

        Returns:
             RDFProperty: Property having the highest similarity degree with the verb.
        """

        best_matched = None

        # E.g.: "Where is Barda Mausoleum located?"
        #   => "Barda Mausoleum"
        if resource_name is not None:
            sparql_query = DBP_PROPERTIES_OF_RESOURCE_QUERY % resource_name
            props = DBpediaQueryService.run_properties_query(sparql_query)
            best_matched = PropertiesMatcher.get_best_matched(props, action, result_type)

        # E.g.: "Where was the person born whose successor was Le Hong Phong?"
        #   => "person"
        else:
            matcher_uri = f'http://localhost:8200/{PATHS.MATCHER}?' \
                          f'{ACCESSORS.QUESTION}={action.sent}&' \
                          f'{ACCESSORS.ACTION_INDEX}={action.i}&' \
                          f'{ACCESSORS.RESULT_TYPE}={result_type}'
            entities_response = requests.get(matcher_uri)
            response = json.loads(entities_response.content)
            prop_json = json.loads(response[ACCESSORS.PROPERTY])
            prop = RDFProperty(
                prop_json["uri"],
                prop_json["parent_uris"],
                prop_json["label"],
                prop_json["ns"],
                prop_json["ns_label"],
                prop_json["res_domain"],
                prop_json["res_range"]
            )
            best_matched = PropertyMatcher(prop, action, result_type)

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

    @staticmethod
    def local_resource_lookup(resource_name):
        """
        Lookup for a specific resource in local files.

        E.g.:
            - question: Who is the tallest basketball player?
            - result: "basketball player" => dbo:BasketballPlayer

        Args:
            resource_name (str): Resource name.

        Returns:
            str: Identified resource.
        """

        filepath = get_dbpedia_file_path("class_list", "csv")
        lines = CSVService.read_lines(filepath)

        for line in lines:
            ns_label, res_label, ns, res, parent_uri = line.split('|')
            # TODO: lookup for similarities
            if res_label.lower() == resource_name.lower():
                return res.replace(ns, ns_label + ":")

        return None


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
    resource_name = noun_chunk.text.title().replace(WORD_SEPARATOR, SPARQL_STR_SEPARATOR)
    resource = LookupService.resource_lookup(resource_name)

    if resource is not None:
        resource_types = []

        uri_translator = URITranslator()
        for parent_uri in resource.parent_uris:
            if parent_uri != ROOT_CLASS_URI:
                resource_types += uri_translator.to_classes([parent_uri])

        resource_types.reverse()
        types += resource_types

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
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.TIME_PERIOD]
    elif label == "EVENT":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.EVENT]
    elif label == "FAC":
        # FAC Buildings, airports, highways, bridges, etc
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.ARCHITECTURAL_STRUCTURE]
    elif label == "GPE" or label == "LOC":
        # GPE Countries, cities, states
        # LOC Non-GPE locations, mountain ranges, bodies of water
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.PLACE]
    elif label == "LANGUAGE":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.LANGUAGE]
    elif label == "LAW":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.LAW]
    elif label == "MONEY":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.CURRENCY]
    elif label == "NORP":
        # Nationalities or religious or political groups
        return [
            item for item in classes if item.uri in [
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.ETHNIC_GROUP,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.POLITICAL_PARTY,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.RELIGIOUS_ORGANISATION
            ]
        ]
    elif label == "ORG":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.ORGANISATION]
    elif label == "PERSON":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.PERSON]
    elif label == "PRODUCT":
        # Objects, vehicles, foods, etc. (Not services)
        return [
            item for item in classes if item.uri in [
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.CHEMICAL_SUBSTANCE,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.DEVICE,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.FLAG,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.FOOD,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.MEAN_OF_TRANSPORTATION,

                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.DATABASE,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.SOFTWARE,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.SPREADSHEET,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.WEBSITE
            ]
        ]
    elif label == "QUANTITY":
        return [
            item for item in classes if item.uri in [
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.ALTITUDE,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.DEPTH,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.GROSS_DOMESTIC_PRODUCT,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.GROSS_DOMESTIC_PRODUCT_PER_CAPITA
            ]
        ]
    elif label == "WORK_OF_ART":
        return [
            item for item in classes if item.uri in [
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.ARTWORK,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.MUSICAL_WORK
            ]
        ]

    # custom labels
    elif label == "CUSTOM_ANATOMY":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.ANATOMICAL_STRUCTURE]
    elif label == "CUSTOM_AWARD":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.AWARD]
    elif label == "CUSTOM_BIOCHEMISTRY":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.BIOMOLECULE]
    elif label == "CUSTOM_CHEMISTRY":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.CHEMICAL_SUBSTANCE]
    elif label == "CUSTOM_CONCEPT":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.TOPICAL_CONCEPT]
    elif label == "CUSTOM_COLOUR":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.COLOUR]
    elif label == "CUSTOM_DISEASE":
        return [
            item for item in classes if item.uri in [
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.DISEASE,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.PANDEMIC
            ]
        ]
    elif label == "CUSTOM_LITERATURE":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.WRITTEN_WORK]
    elif label == "CUSTOM_NAME":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.NAME]
    elif label == "CUSTOM_OCCUPATION":
        return [item for item in classes if item.uri == NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.PERSON_FUNCTION]
    elif label == "CUSTOM_SPECIALISATION":
        return [
            item for item in classes if item.uri in [
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.DIPLOMA,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.MEDICAL_SPECIALTY
            ]
        ]
    elif label == "CUSTOM_RADIO_TV":
        return [
            item for item in classes if item.uri in [
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.FILM,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.RADIO_PROGRAM,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.TELEVISION_EPISODE,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.TELEVISION_SEASON,
                NAMESPACE.DBP_ONTOLOGY + DBPEDIA_CLASS_TYPES.TELEVISION_SHOW
            ]
        ]

    return []
