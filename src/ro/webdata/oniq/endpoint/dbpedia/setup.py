from ro.webdata.oniq.common.print_utils import console
from ro.webdata.oniq.endpoint.common.path_const import CATEGORIES_PATH, CATEGORIES_FILENAME_PREFIX, ENTITIES_PATH
from ro.webdata.oniq.endpoint.common.path_utils import get_filenames
from ro.webdata.oniq.endpoint.common.setup_utils import SetupService
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.endpoint.models.RDFElement import RDFClass, RDFEntity, RDFProperty

_ERROR_COUNTER_THRESHOLD = 10
_TIMEOUT_SECONDS = {
    "DEFAULT": 10,
    "ERROR": 60
}


class DBpediaSetup:
    """
    Service used for caching DBpedia categories, classes and properties.

    Methods:
        init_categories():
            Make a copy of DBP_ONTOLOGY categories to disk.
        init_classes():
            Make a copy of DBP_ONTOLOGY classes to disk.
        init_main_classes():
            Make a copy of DBP_ONTOLOGY main classes to disk.
        init_properties():
            Make a copy of DBP_ONTOLOGY properties to disk.
    """

    @staticmethod
    def init_categories():
        """
        Make a copy of DBP_ONTOLOGY categories to disk.
        """

        counter = DBpediaQueryService.count_categories()
        file_prefix = CATEGORIES_FILENAME_PREFIX
        filename_list = get_filenames(CATEGORIES_PATH, file_prefix)
        headers = RDFClass.get_csv_headers()
        mid_path = "categories/"

        def run_entities_query(offset):
            return DBpediaQueryService.run_categories_query(offset)

        SetupService.write_query_result(counter, filename_list, file_prefix, mid_path, headers, run_entities_query)
        console.info("DBpedia categories has been written to disk!")

    @staticmethod
    def init_classes():
        """
        Make a copy of DBP_ONTOLOGY classes to disk.
        """

        dbo_class_list = DBpediaQueryService.run_classes_query()
        DBpediaQueryService.write_query_result(dbo_class_list, RDFClass.get_csv_headers(), "class_list")
        console.info("DBpedia classes has been written to disk!")

    @staticmethod
    def init_entities(entity_type):
        """
        Extract the entities and make a copy with them.

        Args:
            entity_type (str): Type of entity (E.g.: Organisation, Person, etc.).
        """

        counter = DBpediaQueryService.count_entities(entity_type)
        console.info(f'count({entity_type}) = {counter}')

        file_prefix = entity_type
        filename_list = get_filenames(ENTITIES_PATH + entity_type + "/", file_prefix)
        headers = RDFEntity.get_csv_headers()
        mid_path = "entities/" + entity_type + "/"

        def run_entities_query(offset):
            return DBpediaQueryService.run_entities_query(entity_type, offset)

        SetupService.write_query_result(counter, filename_list, file_prefix, mid_path, headers, run_entities_query)
        console.info(f"DBpedia {entity_type} has been written to disk!")

    @staticmethod
    def init_main_classes():
        """
        Make a copy of DBP_ONTOLOGY main classes to disk.
        A main class is a subclass of **owl:Thing**.
        """

        dbo_class_list = DBpediaQueryService.run_main_classes_query()
        DBpediaQueryService.write_query_result(dbo_class_list, RDFClass.get_csv_headers(), "main_class_list")
        console.info("DBpedia main classes has been written to disk!")

    @staticmethod
    def init_properties():
        """
        Make a copy of DBP_ONTOLOGY properties to disk.
        """

        dbo_prop_list = DBpediaQueryService.run_properties_query()
        DBpediaQueryService.write_query_result(dbo_prop_list, RDFProperty.get_csv_headers(), "prop_list")
        console.info("DBpedia properties has been written to disk!")
