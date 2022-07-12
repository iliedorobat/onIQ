from ro.webdata.oniq.endpoint.common.CSVService import CSV_COLUMN_SEPARATOR
from ro.webdata.oniq.endpoint.common.path_utils import get_dbpedia_file_path
from ro.webdata.oniq.endpoint.common.translator.CSVTranslator import CSVTranslator, CSVBasicTranslator
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements


class TestCSVTranslator:
    @staticmethod
    def run():
        TestCSVTranslator.test_to_categories()
        TestCSVTranslator.test_to_classes()
        TestCSVTranslator.test_to_props()

    @staticmethod
    def test_to_categories():
        # categories = CSVTranslator.to_categories()

        categories = []
        # Performance reason: prevent parsing all the categories files
        filename = "category_list_0"
        filepath = get_dbpedia_file_path(filename, "csv", "categories/")
        categories += CSVBasicTranslator.csv_file_to_categories(filepath, True, CSV_COLUMN_SEPARATOR)

        rdf_categories = RDFElements(categories)

        print(
            f'test_to_categories():\n'
            f'\t{rdf_categories}'
        )

    @staticmethod
    def test_to_classes():
        rdf_classes = CSVTranslator.to_classes(False, CSV_COLUMN_SEPARATOR)
        print(
            f'test_to_classes():\n'
            f'\t{rdf_classes}'
        )

    @staticmethod
    def test_to_props():
        rdf_props = CSVTranslator.to_props(False, CSV_COLUMN_SEPARATOR)
        print(
            f'test_to_props():\n'
            f'\t{rdf_props}'
        )


class TestCSVBasicTranslator:
    @staticmethod
    def run():
        TestCSVBasicTranslator.test_csv_file_to_categories()
        TestCSVBasicTranslator.test_csv_file_to_classes()
        TestCSVBasicTranslator.test_csv_file_to_props()
        TestCSVBasicTranslator.test_csv_file_to_custom_props()

    @staticmethod
    def test_csv_file_to_categories():
        filepath = get_dbpedia_file_path("category_list_0", "csv", "categories/")
        rdf_categories = CSVBasicTranslator.csv_file_to_categories(filepath, False, CSV_COLUMN_SEPARATOR)

        print(
            f'test_csv_file_to_categories():\n'
            f'\t{rdf_categories}'
        )

    @staticmethod
    def test_csv_file_to_classes():
        filepath = get_dbpedia_file_path("class_list", "csv")
        rdf_classes = CSVBasicTranslator.csv_file_to_classes(filepath, False, CSV_COLUMN_SEPARATOR)

        print(
            f'test_csv_file_to_classes():\n'
            f'\t{RDFElements(rdf_classes)}'
        )

    @staticmethod
    def test_csv_file_to_props():
        filepath = get_dbpedia_file_path("prop_list", "csv")
        rdf_props = CSVBasicTranslator.csv_file_to_props(filepath, False, CSV_COLUMN_SEPARATOR)

        print(
            f'test_csv_file_to_props():\n'
            f'\t{RDFElements(rdf_props)}'
        )

    @staticmethod
    def test_csv_file_to_custom_props():
        classes_filepath = get_dbpedia_file_path("class_list", "csv")
        rdf_props = CSVBasicTranslator.csv_file_to_custom_props(classes_filepath, False, CSV_COLUMN_SEPARATOR)

        print(
            f'test_csv_file_to_custom_props():\n'
            f'\t{RDFElements(rdf_props)}'
        )

