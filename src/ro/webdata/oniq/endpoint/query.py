from typing import List, Union

import pydash
# https://rdflib.dev/sparqlwrapper/
from SPARQLWrapper import SPARQLWrapper, JSON

from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.endpoint.common.translator.URITranslator import URITranslator
from ro.webdata.oniq.endpoint.common.CSVService import CSV_COLUMN_SEPARATOR
from ro.webdata.oniq.endpoint.models.RDFElement import RDFCategory, RDFClass, RDFProperty
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.endpoint.sparql_query import CATEGORIES_COUNTER_QUERY, CATEGORIES_QUERY, CLASSES_QUERY, \
    PROPERTIES_OF_RESOURCE_QUERY, PROPERTIES_QUERY, RESOURCE_QUERY


CLASSES_HEADERS = ['namespace label', 'resource label', 'namespace', 'resource uri', 'parent uri']
PROPERTIES_HEADERS = ['namespace label', 'resource label', 'namespace', 'resource uri', 'parent uri', 'domain', 'range']


class QueryService:
    """
    Service used for querying a specific endpoint.

    Methods:
        run_query(endpoint, query):
            Query the target endpoint.
        get_categories_counter(endpoint, sparql_query=CATEGORIES_COUNTER_QUERY):
            Query the target endpoint to get the number of categories.
        run_categories_query(endpoint, category_ns, sparql_query=CATEGORIES_QUERY, offset=0):
            Query the target endpoint to get the list of categories.
        run_classes_query(endpoint, sparql_query=CLASSES_QUERY):
            Query the target endpoint to get the list of classes.
        run_properties_query(endpoint, sparql_query=PROPERTIES_QUERY):
            Query the target endpoint to get the list of properties.
        run_resources_query(endpoint, sparql_query=CLASSES_QUERY):
            Query the target endpoint to get the list of matched resources
        run_resource_query(endpoint, resource_name=None, sparql_query=RESOURCE_QUERY):
            Query the target endpoint to get a specific resource.
        write_query_result(resource_list, headers, filepath):
            Save the queried resources to disk.
    """

    @staticmethod
    def run_query(endpoint, query):
        """
        Query the target endpoint.

        Args:
            endpoint (str): Communication channel.
            query (str): SPARQL query.

        Returns:
            dict: Queried resources.
        """

        sparql = SPARQLWrapper(endpoint)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        return sparql.query().convert()

    @staticmethod
    def get_categories_counter(endpoint, sparql_query=CATEGORIES_COUNTER_QUERY):
        """
        Query the target endpoint to get the number of categories.

        Args:
            endpoint (str): Communication channel.
            sparql_query (str): SPARQL query.

        Returns:
            int: Number of categories.
        """

        counter = 0
        response = QueryService.run_query(endpoint, sparql_query)

        for result in response["results"]["bindings"]:
            counter = int(result["counter"]["value"])

        return counter

    @staticmethod
    def run_categories_query(endpoint, category_ns, sparql_query=CATEGORIES_QUERY, offset=0):
        """
        Query the target endpoint to get the list of categories.

        Args:
            endpoint (str): Communication channel.
            category_ns (str): Category namespace (E.g.: NAMESPACE.DBP_CATEGORY).
            sparql_query (str): SPARQL query.
            offset (int): Skip "offset" tuples from the total result set.

        Returns:
            RDFElements[RDFClass]: Sorted list of unique categories.
        """

        categories = RDFElements([])
        response = QueryService.run_query(endpoint, sparql_query % offset)

        for result in response["results"]["bindings"]:
            label = result["label"]["value"]
            uri = result["class"]["value"]
            categories.append(
                RDFClass(uri, [], label, category_ns)
            )

        categories.unique()
        categories.sort()

        return categories

    @staticmethod
    def run_classes_query(endpoint, sparql_query=CLASSES_QUERY):
        """
        Query the target endpoint to get the list of classes.

        Args:
            endpoint (str): Communication channel.
            sparql_query (str): SPARQL query.

        Returns:
            RDFElements[RDFClass]: The list of classes.
        """

        classes = RDFElements([])
        response = QueryService.run_query(endpoint, sparql_query)

        for result in response["results"]["bindings"]:
            label = result["label"]["value"]
            uri = result["class"]["value"]
            parent_uri = result["subclassOf"]["value"]
            ns = result["namespace"]["value"]

            if classes.exists(uri):
                rdf_class = classes.find(uri)
                rdf_class.parent_uris.append(parent_uri)
            else:
                classes.append(
                    RDFClass(uri, [parent_uri], label, ns)
                )

        classes.unique()
        classes.sort()

        return classes

    @staticmethod
    def run_properties_query(endpoint, sparql_query=PROPERTIES_QUERY):
        """
        Query the target endpoint to get the list of properties.

        Args:
            endpoint (str): Communication channel.
            sparql_query (str): SPARQL query.

        Returns:
            RDFElements[RDFProperty]: The list of properties.
        """

        properties = RDFElements([])
        response = QueryService.run_query(endpoint, sparql_query)

        for result in response["results"]["bindings"]:
            label = pydash.get(result, ["label", "value"])
            uri = result["property"]["value"]
            parent_uri = pydash.get(result, ["subclassOf", "value"])
            parent_uris = [parent_uri] if parent_uri is not None else []
            res_domain = pydash.get(result, ["domain", "value"])
            res_range = pydash.get(result, ["range", "value"])

            properties.append(
                RDFProperty(uri, parent_uris, label, res_domain=res_domain, res_range=res_range)
            )

        properties.unique()
        properties.sort()

        return properties

    @staticmethod
    def run_resources_query(endpoint, sparql_query=CLASSES_QUERY):
        """
        Query the target endpoint to get the list of matched resources.

        Args:
            endpoint (str): Communication channel.
            sparql_query (str): SPARQL query.

        Returns:
            RDFElements[RDFClass]: List of classes.
        """

        classes = RDFElements([])
        response = QueryService.run_query(endpoint, sparql_query)
        uri_translator = URITranslator()

        for result in response["results"]["bindings"]:
            label = pydash.get(result, ["label", "value"])
            uri = result["class"]["value"]
            parent_uri = pydash.get(result, ["subclassOf", "value"])

            if classes.exists(uri):
                rdf_class = classes.find(uri)

                if parent_uri is not None and (
                    NAMESPACE.DBP_ONTOLOGY in parent_uri or
                    NAMESPACE.OWL in parent_uri
                ):
                    rdf_class.parent_uris.append(parent_uri)
            else:
                rdf_class = uri_translator.to_class(uri)

                if rdf_class is not None:
                    parent_uris = rdf_class.parent_uris
                else:
                    if parent_uri is not None and (
                        NAMESPACE.DBP_ONTOLOGY in parent_uri or
                        NAMESPACE.OWL in parent_uri
                    ):
                        parent_uris = [parent_uri]
                    else:
                        parent_uris = []

                classes.append(
                    RDFClass(uri, parent_uris, label)
                )

        classes.unique()
        classes.sort()

        return classes

    @staticmethod
    def run_resource_query(endpoint, resource_name=None, sparql_query=RESOURCE_QUERY):
        """
        Query the target endpoint to get a specific resource.

        Args:
            endpoint (str): Communication channel.
            resource_name (str): Name of the resource (E.g.: "Barda_Mausoleum").
            sparql_query (str): SPARQL query.

        Returns:
            RDFClass: Queried resource.
        """

        if resource_name is None or len(resource_name) == 0:
            return None

        query = sparql_query % resource_name
        result = QueryService.run_resources_query(endpoint, query)

        if len(result) == 1:
            return result[0]

        return None

    @staticmethod
    def run_resource_properties_query(endpoint, resource_name=None, sparql_query=PROPERTIES_OF_RESOURCE_QUERY):
        """
        Query the target endpoint to get the list of properties of a specific resource.

        Args:
            endpoint (str): Communication channel.
            resource_name (str): Name of the target resource (E.g.: "Barda_Mausoleum").
            sparql_query (str): SPARQL query.

        Returns:
            RDFElements[RDFProperty]: The list of properties.
        """

        if resource_name is None or len(resource_name) == 0:
            return None

        props = RDFElements([])
        query = sparql_query % resource_name
        response = QueryService.run_query(endpoint, query)
        results = pydash.get(response, ["results", "bindings"], [])

        for result in results:
            label = pydash.get(result, ["label", "value"])
            uri = pydash.get(result, ["property", "value"])
            res_domain = pydash.get(result, ["domain", "value"])
            res_range = pydash.get(result, ["range", "value"])
            parent_uri = pydash.get(result, ["subclassOf", "value"])
            parent_uris = [parent_uri] if parent_uri is not None else []
            props.append(
                RDFProperty(uri, parent_uris, label, res_domain=res_domain, res_range=res_range)
            )

        props.unique()
        props.sort()

        return props

    @staticmethod
    def write_query_result(resource_list, headers, filepath):
        """
        Save the queried resources to disk.

        Args:
            resource_list (List[RDFCategory, RDFClass, RDFProperty]):
                List of resources (lookup to QueryService.run_classes_query() etc.).
            headers (List[str]):
                Name of the columns.
            filepath (str):
                Absolute path (including the filename and extension).
        """

        file = open(filepath, "w+")
        file.write(CSV_COLUMN_SEPARATOR.join(headers) + "\n")

        for resource in resource_list:
            file.write(resource.to_csv() + "\n")

        file.close()
