from ro.webdata.oniq.endpoint.dbpedia.constants import DBPEDIA_CLASS_TYPES
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_RESOURCE_QUERY, DBP_ONTOLOGY_RESOURCE_QUERY
from ro.webdata.test.oniq.common.print_utils import print_not_implemented


class TestDBpediaQueryService:
    @staticmethod
    def run():
        TestDBpediaQueryService.test_count_categories()
        TestDBpediaQueryService.test_count_entities()
        TestDBpediaQueryService.test_run_categories_query()
        TestDBpediaQueryService.test_run_classes_query()
        TestDBpediaQueryService.test_run_main_classes_query()
        TestDBpediaQueryService.test_run_properties_query()
        TestDBpediaQueryService.test_run_resource_query()
        TestDBpediaQueryService.test_write_query_result()

    @staticmethod
    def test_count_categories():
        categories_counter = DBpediaQueryService.count_categories()
        print(
            f'count_categories():\n'
            f'\tcategories_counter: {categories_counter}'
        )

    @staticmethod
    def test_count_entities():
        counter_resp = DBpediaQueryService.count_entities(DBPEDIA_CLASS_TYPES.ORGANISATION)
        print(
            f'count_entities("{DBPEDIA_CLASS_TYPES.ORGANISATION}"):\n'
            f'\tentities_counter: {counter_resp}'
        )

    @staticmethod
    def test_run_categories_query():
        categories = DBpediaQueryService.run_categories_query()
        print(
            f'run_categories_query():\n'
            f'\tlen(categories): {len(categories)}'
        )

    @staticmethod
    def test_run_classes_query():
        classes = DBpediaQueryService.run_classes_query()
        print(
            f'run_classes_query():\n'
            f'\tlen(classes): {len(classes)}'
        )

    @staticmethod
    def test_run_main_classes_query():
        main_classes = DBpediaQueryService.run_main_classes_query()
        print(
            f'run_main_classes_query():\n'
            f'\tlen(main_classes): {len(main_classes)}'
        )

    @staticmethod
    def test_run_properties_query():
        properties = DBpediaQueryService.run_properties_query()
        print(
            f'run_properties_query():\n'
            f'\tlen(properties): {len(properties)}'
        )

    @staticmethod
    def test_run_resource_query():
        band = DBpediaQueryService.run_resource_query("Band", DBP_ONTOLOGY_RESOURCE_QUERY)
        monument = DBpediaQueryService.run_resource_query("Monument", DBP_ONTOLOGY_RESOURCE_QUERY)
        museum = DBpediaQueryService.run_resource_query("Museum", DBP_ONTOLOGY_RESOURCE_QUERY)
        barda_mausoleum = DBpediaQueryService.run_resource_query("Barda_Mausoleum", DBP_RESOURCE_QUERY)

        print(
            f'run_resource_query():\n'
            f'\tBand: {band}\n'
            f'\tMonument: {monument}\n'
            f'\tMuseum: {museum}'
            f'\tBarda_Mausoleum: {barda_mausoleum}'
        )

    @staticmethod
    def test_write_query_result():
        print_not_implemented("test_write_query_result")
