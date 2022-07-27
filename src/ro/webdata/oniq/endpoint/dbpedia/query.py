from ro.webdata.oniq.endpoint.common.path_utils import get_dbpedia_file_path
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBO_CATEGORIES_COUNTER_QUERY, DBO_CATEGORIES_QUERY, \
    DBO_CLASSES_QUERY, DBO_MAIN_CLASSES_QUERY, DBO_PROPERTIES_QUERY, DBP_ENDPOINT, DBP_ENTITY_TYPE_COUNTER_QUERY, \
    DBP_ENTITY_TYPE_QUERY, DBP_PROPERTIES_OF_RESOURCE_QUERY
from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.endpoint.query import QueryService


class DBpediaQueryService:
    """
    Service used for querying the DBpedia endpoint.

    Methods:
        count_categories():
            Query DBpedia to get the number of categories.
        count_entities(entity_type):
            Query DBpedia to get the number of entities.
        run_categories_query(offset=0):
            Query DBpedia to get the list of DBP_ONTOLOGY categories.
        run_entities_query(entity_type, offset=0):
            Query DBpedia to get the list of DBP_ONTOLOGY entities.
        run_classes_query():
            Query DBpedia to get the list of DBP_ONTOLOGY classes.
        run_main_classes_query():
            Query DBpedia to get the list of DBP_ONTOLOGY main classes.
        run_properties_query(sparql_query=DBO_PROPERTIES_QUERY):
            Query DBpedia to get the list of DBP_ONTOLOGY properties.
        run_resource_query(resource_name, sparql_query):
            Query DBpedia to get a specific DBP_ONTOLOGY / DBP_RESOURCE resource.
        write_query_result(resource_list, headers, filename, mid_path=""):
            Save the queried resources to disk.
    """

    @staticmethod
    def count_categories():
        """
        Query DBpedia to get the number of categories.

        Returns:
            int: The number of categories.
        """

        return QueryService.count_resources(DBP_ENDPOINT, DBO_CATEGORIES_COUNTER_QUERY)

    @staticmethod
    def count_entities(entity_type):
        """
        Query DBpedia to get the number of entities.

        Args:
            entity_type (str): Type of entity (E.g.: Organisation, Person, etc.).

        Returns:
            int: The number of entities.
        """

        query = DBP_ENTITY_TYPE_COUNTER_QUERY % entity_type

        return QueryService.count_resources(DBP_ENDPOINT, query)

    @staticmethod
    def run_categories_query(offset=0):
        """
        Query DBpedia to get the list of DBP_ONTOLOGY categories.

        E.g.:
            - "Which Italian dessert contains coffee?"
                => "Italian dessert" -> http://dbpedia.org/page/Category:Italian_desserts

        Args:
            offset (int): Skip "offset" tuples from the total result set.

        Returns:
            RDFElements[RDFCategory]: Sorted list of unique DBP_ONTOLOGY categories.
        """

        return QueryService.run_categories_query(DBP_ENDPOINT, NAMESPACE.DBP_CATEGORY, DBO_CATEGORIES_QUERY, offset)

    @staticmethod
    def run_entities_query(entity_type, offset=0):
        """
        Query DBpedia to get the list of DBP_ONTOLOGY entities.

        Args:
            entity_type (str): Type of entity (E.g.: Organisation, Person, etc.).
            offset (int): Skip "offset" tuples from the total result set.

        Returns:
            RDFElements[RDFEntity]: Sorted list of unique DBP_ONTOLOGY entities.
        """

        return QueryService.run_entities_query(DBP_ENDPOINT, NAMESPACE.DBP_ONTOLOGY, DBP_ENTITY_TYPE_QUERY, entity_type, offset)

    @staticmethod
    def run_classes_query():
        """
        Query DBpedia to get the list of DBP_ONTOLOGY classes.

        Returns:
            RDFElements[RDFClass]: The list of DBP_ONTOLOGY classes.
        """

        return QueryService.run_classes_query(DBP_ENDPOINT, DBO_CLASSES_QUERY)

    @staticmethod
    def run_main_classes_query():
        """
        Query DBpedia to get the list of DBP_ONTOLOGY main classes.
        A main class is a subclass of **owl:Thing**.

        Returns:
            RDFElements[RDFClass]: The list of DBP_ONTOLOGY main classes.
        """

        return QueryService.run_classes_query(DBP_ENDPOINT, DBO_MAIN_CLASSES_QUERY)

    @staticmethod
    def run_properties_query(sparql_query=DBO_PROPERTIES_QUERY):
        """
        Query DBpedia to get the list of DBP_ONTOLOGY properties.

        Args:
            sparql_query (str): SPARQL query (E.g.: DBO_PROPERTIES_QUERY,
                DBP_PROPERTIES_OF_RESOURCE_QUERY).

        Returns:
            RDFElements[RDFProperty]: The list of DBP_ONTOLOGY properties.
        """

        return QueryService.run_properties_query(DBP_ENDPOINT, sparql_query)

    @staticmethod
    def run_resource_query(resource_name, sparql_query):
        """
        Query DBpedia to get a specific DBP_ONTOLOGY / DBP_RESOURCE resource.

        E.g.:
            - DBP_ONTOLOGY resource's name: "Museum", "Mausoleum", etc.
            - DBP_RESOURCE resource's name: "Barda_Mausoleum"

        Args:
            resource_name (str): Name of resource being queried (E.g.: "Museum",
                "Mausoleum", "Barda_Mausoleum", etc.).
            sparql_query (str): SPARQL query (E.g.: DBP_ONTOLOGY_RESOURCE_QUERY,
                DBP_RESOURCE_QUERY).

        Returns:
            RDFClass: Queried DBP_ONTOLOGY / DBP_RESOURCE resource.
        """

        return QueryService.run_resource_query(DBP_ENDPOINT, resource_name, sparql_query)

    @staticmethod
    def run_resource_properties_query(resource_name):
        """
        Query DBpedia to get the list of properties of a specific resource.

        Args:
            resource_name (str): Name of the target resource (E.g.: "Barda_Mausoleum").

        Returns:
            RDFElements[RDFProperty]: The list of properties.
        """

        return QueryService.run_resource_properties_query(DBP_ENDPOINT, resource_name, DBP_PROPERTIES_OF_RESOURCE_QUERY)

    @staticmethod
    def write_query_result(resource_list, headers, filename, mid_path=""):
        """
        Save the queried resources to disk.

        Args:
            resource_list (List[RDFCategory, RDFClass, RDFProperty]):
                List of resources (lookup to QueryService.run_classes_query() etc.).
            headers (List[str]):
                Name of the columns.
            filename (str):
                Name of the file.
            mid_path (str):
                Path between DBpedia directory and the file.
                E.g.:
                    - get_dbpedia_file_path(filename, "csv", "categories/");
                    - get_dbpedia_file_path(filename, "csv", "entities/Person/").
        """

        filepath = get_dbpedia_file_path(filename, "csv", mid_path)
        QueryService.write_query_result(resource_list, headers, filepath)
