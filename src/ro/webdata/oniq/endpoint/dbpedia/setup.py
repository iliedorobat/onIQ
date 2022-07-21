import time
from urllib.error import HTTPError, URLError

from SPARQLWrapper.SPARQLExceptions import EndPointInternalError

from ro.webdata.oniq.common.print_utils import console
from ro.webdata.oniq.endpoint.common.path_utils import filename_to_number, get_categories_filenames
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_OFFSET
from ro.webdata.oniq.endpoint.query import CLASSES_HEADERS, PROPERTIES_HEADERS

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

        write_categories_result()
        print("DBpedia categories has been written to disk!")

    @staticmethod
    def init_classes():
        """
        Make a copy of DBP_ONTOLOGY classes to disk.
        """

        dbo_class_list = DBpediaQueryService.run_classes_query()
        DBpediaQueryService.write_query_result(dbo_class_list, CLASSES_HEADERS, "class_list")
        print("DBpedia classes has been written to disk!")

    @staticmethod
    def init_main_classes():
        """
        Make a copy of DBP_ONTOLOGY main classes to disk.
        A main class is a subclass of **owl:Thing**.
        """

        dbo_class_list = DBpediaQueryService.run_main_classes_query()
        DBpediaQueryService.write_query_result(dbo_class_list, CLASSES_HEADERS, "main_class_list")
        print("DBpedia main classes has been written to disk!")

    @staticmethod
    def init_properties():
        """
        Make a copy of DBP_ONTOLOGY properties to disk.
        """

        dbo_prop_list = DBpediaQueryService.run_properties_query()
        DBpediaQueryService.write_query_result(dbo_prop_list, PROPERTIES_HEADERS, "prop_list")
        print("DBpedia properties has been written to disk!")


def write_categories_result():
    counter = DBpediaQueryService.get_categories_counter()
    meta = {
        "error_counter": 0,
        "i": 1,
        "offset": _get_startup_offset()
    }

    while counter > meta["offset"]:
        _write_categories(meta)

    missing_offset_list = _get_missing_offsets(counter)
    while len(missing_offset_list) > 0:
        for offset in missing_offset_list:
            meta["offset"] = offset
            _write_categories(meta)
        missing_offset_list = _get_missing_offsets(counter)


def _get_missing_offsets(counter):
    """
    Read filenames from "files/dbpedia/categories" to retrieve missing offsets

    :param counter: Total number of categories
    :return: List of missing offsets
    """

    missing_offset_list = []
    offset_list = _get_offsets()
    offset_list.append(counter)

    # insert "0" offset to "offset_list" on the first position if it does not already exist
    if len(offset_list) > 0 and offset_list[0] != 0:
        missing_offset_list.append(0)
        offset_list.insert(0, 0)

    for index in range(1, len(offset_list)):
        if offset_list[index] - offset_list[index - 1] >= DBP_OFFSET:
            min_offset = offset_list[index - 1]
            next_offset = min_offset + DBP_OFFSET
            max_offset = offset_list[index]

            while next_offset < max_offset:
                missing_offset_list.append(next_offset)
                next_offset += DBP_OFFSET

    return missing_offset_list


def _get_startup_offset():
    """
    Read filenames from "files/dbpedia/categories" to retrieve the startup offset
    (start offset = last offset + DBP_OFFSET)

    :return: The starting offset
    """

    offset_list = _get_offsets()

    if len(offset_list) > 0:
        return offset_list[len(offset_list) - 1] + DBP_OFFSET

    return 0


def _get_offsets():
    filename_list = get_categories_filenames()
    offset_list = []

    for filename in filename_list:
        offset = filename_to_number(filename)

        if offset is not None:
            offset_list.append(offset)

    return sorted(offset_list)


def _write_categories(meta, timeout=_TIMEOUT_SECONDS["DEFAULT"]):
    """
    Query for categories against DBpedia and write the result to disk

    :param meta: A dictionary containing "error_counter", current index ("i") and the current offset ("offset")
        E.g.:
        {
            "error_counter": 0,
            "i": 3,
            "offset": 10000
        }
    :param timeout: Timeout interval (in seconds) between two queries
    :return: None
    """

    try:
        if meta["error_counter"] < _ERROR_COUNTER_THRESHOLD:
            console.info(f"{meta['i']}. QUERYING: DBpedia categories with offset={meta['offset']}")
            time.sleep(timeout)
            categories_list = DBpediaQueryService.run_categories_query(meta["offset"])
            DBpediaQueryService.write_query_result(
                categories_list,
                CLASSES_HEADERS,
                f"category_list_{meta['offset']}",
                "categories/"
            )
            console.debug(f"{meta['i']}. PASSED: DBpedia categories query with offset={meta['offset']}")

        meta["i"] += 1
        meta["error_counter"] = 0
        meta["offset"] += DBP_OFFSET
    except (TimeoutError, EndPointInternalError, HTTPError, URLError):
        meta["error_counter"] += 1

        if meta["error_counter"] == _ERROR_COUNTER_THRESHOLD:
            console.error(f"{meta['i']}. FAILED: DBpedia categories query with offset={meta['offset']}")
        else:
            console.warning(f"{meta['i']}. Restoring the connection with offset={meta['offset']}...")

        _write_categories(meta, _TIMEOUT_SECONDS["ERROR"])
