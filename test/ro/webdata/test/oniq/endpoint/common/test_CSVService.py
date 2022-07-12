from ro.webdata.oniq.endpoint.common.CSVService import CSVService
from ro.webdata.oniq.endpoint.common.path_utils import get_dbpedia_file_path


class TestCSVService:
    @staticmethod
    def run():
        TestCSVService.test_read_lines()

    @staticmethod
    def test_read_lines():
        filepath = get_dbpedia_file_path("category_list_0", "csv", "categories/")
        lines = CSVService.read_lines(filepath)

        print(f'read_lines():\n')
        for line in lines:
            print(f'\t{line}')
