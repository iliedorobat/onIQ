from typing import List

import pydash
# https://rdflib.dev/sparqlwrapper/
from SPARQLWrapper import SPARQLWrapper, JSON

from ro.webdata.oniq.endpoint.common.CSVService import CSV_COLUMN_SEPARATOR
from ro.webdata.oniq.endpoint.common.translator.URITranslator import URITranslator
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_RESOURCE_TYPE_QUERY, DBP_PROPERTY_RANGE_QUERY
from ro.webdata.oniq.endpoint.models.RDFElement import RDFCategory, RDFClass, RDFEntity, RDFProperty
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.endpoint.sparql_query import CATEGORIES_QUERY, CLASSES_QUERY, \
    PROPERTIES_OF_RESOURCE_QUERY, PROPERTIES_QUERY, RESOURCE_QUERY


class QueryService:
    """
    Service used for querying a specific endpoint.

    Methods:
        run_query(endpoint, query):
            Query the target endpoint.
        count_categories(endpoint, sparql_query=CATEGORIES_COUNTER_QUERY):
            Query the target endpoint to get the number of categories.
        run_categories_query(endpoint, category_ns, sparql_query=CATEGORIES_QUERY, offset=0):
            Query the target endpoint to get the list of categories.
        run_classes_query(endpoint, sparql_query=CLASSES_QUERY):
            Query the target endpoint to get the list of classes.
        run_properties_query(endpoint, sparql_query=PROPERTIES_QUERY):
            Query the target endpoint to get the list of properties.
        run_resource_type_query(endpoint, resource_name=None, sparql_query=DBP_RESOURCE_TYPE_QUERY):
            Query the target endpoint to get the list of parent classes of a specific resource.
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
    def count_resources(endpoint, sparql_query):
        """
        Query the target endpoint to get the number of resources.

        Args:
            endpoint (str): Communication channel.
            sparql_query (str): SPARQL query.

        Returns:
            int: Number of resources.
        """

        response = QueryService.run_query(endpoint, sparql_query)

        count_json = pydash.get(response, ["results", "bindings", 0, "count"], {})
        count_type = pydash.get(count_json, "datatype")

        if count_type != "http://www.w3.org/2001/XMLSchema#integer":
            return 0

        count_value = pydash.get(count_json, "value", 0)

        return int(count_value)

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
            RDFElements[RDFCategory]: Sorted list of unique categories.
        """

        categories = RDFElements([])
        response = QueryService.run_query(endpoint, sparql_query % offset)

        for result in response["results"]["bindings"]:
            label = result["label"]["value"]
            uri = result["class"]["value"]
            categories.append(
                RDFCategory(uri, [], label, category_ns)
            )

        categories.unique()
        categories.sort()

        return categories

    @staticmethod
    def run_entities_query(endpoint, namespace, sparql_query, entity_type, offset=0):
        """
        Query the target endpoint to get the list of entities.

        Args:
            endpoint (str): Communication channel.
            namespace (str): Entity namespace (E.g.: NAMESPACE.DBP_CATEGORY).
            sparql_query (str): SPARQL query.
            entity_type (str): Type of entity (E.g.: Organisation, Person, etc.).
            offset (int): Skip "offset" tuples from the total result set.

        Returns:
            RDFElements[RDFEntity]: Sorted list of unique entities.
        """

        entities = RDFElements([])
        response = QueryService.run_query(endpoint, sparql_query % (entity_type, offset))
        results = pydash.get(response, ["results", "bindings"], [])

        for result in results:
            label = pydash.get(result, ["label", "value"])
            name = pydash.get(result, ["name", "value"])
            uri = pydash.get(result, ["resource", "value"])
            res_type = NAMESPACE.DBP_ONTOLOGY + entity_type
            entities.append(
                RDFEntity(uri, label, name, res_type, namespace)
            )

        entities.unique()
        entities.sort()

        return entities

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
    def run_resource_type_range(endpoint, prop=None, sparql_query=DBP_PROPERTY_RANGE_QUERY):
        if prop is None or len(prop) == 0:
            return None

        ranges = []
        query = sparql_query % escape_resource_name(prop)
        response = QueryService.run_query(endpoint, query)

        for result in response["results"]["bindings"]:
            prop_range = pydash.get(result, ["range", "value"])
            ranges.append(prop_range)

        return ranges

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
    def run_resource_type_query(endpoint, resource_name=None, sparql_query=DBP_RESOURCE_TYPE_QUERY):
        """
        Query the target endpoint to get the list of parent classes of a specific resource.

        Args:
            endpoint (str): Communication channel.
            resource_name (str): Name of the resource (E.g.: "Pulitzer_Prize").
            sparql_query (str): SPARQL query.

        Returns:
            List[str]: List of parent classes.
        """

        if resource_name is None or len(resource_name) == 0:
            return None

        # TODO: classes = RDFElements([])
        classes = []
        query = sparql_query % escape_resource_name(resource_name)
        response = QueryService.run_query(endpoint, query)

        for result in response["results"]["bindings"]:
            rdf_class = pydash.get(result, ["class", "value"])
            classes.append(rdf_class)

        return classes

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

        query = sparql_query % escape_resource_name(resource_name)
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
        query = sparql_query % escape_resource_name(resource_name)
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


def escape_resource_name(resource_name: str):
    # E.g.: "New_York_(state)" => "New_York_\(state\)"
    res_name = resource_name.replace("(", "\(").replace(")", "\)")

    # E.g.: "Pulitzer Prize" => "Pulitzer_Prize"
    res_name = res_name.replace(" ", "_")

    # E.g.: "Apple_Inc." => "Apple_Inc\."
    res_name = res_name.replace(".", "\.")

    # E.g.: "how much is the total population of  european union?"
    res_name = res_name.replace("'", "\'")

    return res_name
