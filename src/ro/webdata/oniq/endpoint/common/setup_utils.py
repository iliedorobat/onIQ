from typing import List
from urllib.error import HTTPError, URLError

import time
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError

from ro.webdata.oniq.common.print_utils import console
from ro.webdata.oniq.endpoint.common.path_utils import filename_to_number
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_OFFSET

_ERROR_COUNTER_THRESHOLD = 10
_TIMEOUT_SECONDS = {
    "DEFAULT": 10,
    "ERROR": 60
}


class SetupService:
    @staticmethod
    def get_offsets(filename_list, prefix):
        offset_list = []

        for filename in filename_list:
            offset = filename_to_number(filename, prefix)

            if offset is not None:
                offset_list.append(offset)

        return sorted(offset_list)

    @staticmethod
    def get_missing_offsets(total, filename_list, file_prefix):
        """
        Read every file from the list of files to retrieve the missing offsets.

        Args:
            total (int): Total number of resources.
            filename_list (List[str]): List of file names.
            file_prefix (str): String from the beginning of the file which will
                be removed to determine the integer (check <b>filename_to_number</b>).

        Returns:
            List[int]: List of missing offsets.
        """

        missing_offset_list = []
        offset_list = SetupService.get_offsets(filename_list, file_prefix)
        offset_list.append(total)

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

    @staticmethod
    def get_startup_offset(filename_list, file_prefix):
        """
        Read every file from the list of files to retrieve the startup offset
        (start offset = last offset + DBP_OFFSET)

        Args:
            filename_list (List[str]): List of file names.
            file_prefix (str): String from the beginning of the file which will
                be removed to determine the integer (check <b>filename_to_number</b>).

        :return: The starting offset
        """

        offset_list = SetupService.get_offsets(filename_list, file_prefix)

        if len(offset_list) > 0:
            return offset_list[len(offset_list) - 1] + DBP_OFFSET

        return 0

    @staticmethod
    def write_query_result(total, filename_list, file_prefix, mid_path, headers, run_query):
        """
        Query for resources against DBpedia and write the result to disk.

        Args:
            total (int): Total number of resources.
            filename_list (List[str]): List of file names.
            file_prefix (str): String from the beginning of the file which will
                be removed to determine the integer (check <b>filename_to_number</b>).
            mid_path (str):
                Path between DBpedia directory and the file.
                E.g.:
                    - get_dbpedia_file_path(filename, "csv", "categories/");
                    - get_dbpedia_file_path(filename, "csv", "entities/").
            headers (List[str]):
                List of CSV headers.
                E.g.: RDF.Entity.get_csv_headers().
            run_query (function):
                Method used for querying resources.
                E.g.:
                    - DBpediaQueryService.run_categories_query
                    - DBpediaQueryService.run_entities_query
        :return:
        """

        meta = {
            "error_counter": 0,
            "i": 1,
            "offset": SetupService.get_startup_offset(filename_list, file_prefix)
        }

        while total > meta["offset"]:
            _write_query_result(meta, file_prefix, mid_path, headers, run_query)

        missing_offset_list = SetupService.get_missing_offsets(total, filename_list, file_prefix)
        while len(missing_offset_list) > 0:
            for offset in missing_offset_list:
                meta["offset"] = offset
                _write_query_result(meta, file_prefix, mid_path, headers, run_query)
            missing_offset_list = SetupService.get_missing_offsets(total, filename_list, file_prefix)


def _write_query_result(meta, file_prefix, mid_path, headers, run_query, timeout=_TIMEOUT_SECONDS["DEFAULT"]):
    """
    Query for resources against DBpedia and write the result to disk.

    Args:
        meta (Dict):
            Dictionary containing "error_counter", current index ("i")
            and the current offset ("offset").
            E.g.:
                {
                    "error_counter": 0,
                    "i": 3,
                    "offset": 10000
                }
        file_prefix (str): String from the beginning of the file which will
            be removed to determine the integer (check <b>filename_to_number</b>).
        mid_path (str):
            Path between DBpedia directory and the file.
            E.g.:
                - get_dbpedia_file_path(filename, "csv", "categories/");
                - get_dbpedia_file_path(filename, "csv", "entities/").
        headers (List[str]):
            List of CSV headers.
            E.g.: RDF.Entity.get_csv_headers().
        run_query (function):
            Method used for querying resources.
            E.g.:
                - DBpediaQueryService.run_categories_query
                - DBpediaQueryService.run_entities_query
        timeout (int):
            Timeout interval (in seconds) between two queries
    """

    try:
        if meta["error_counter"] < _ERROR_COUNTER_THRESHOLD:
            console.info(f"{meta['i']}. QUERYING: DBpedia with offset={meta['offset']}")
            time.sleep(timeout)
            resources = run_query(meta["offset"])
            DBpediaQueryService.write_query_result(
                resources,
                headers,
                f"{file_prefix}{meta['offset']}",
                mid_path
            )
            console.debug(f"{meta['i']}. PASSED: DBpedia query with offset={meta['offset']}")

        meta["i"] += 1
        meta["error_counter"] = 0
        meta["offset"] += DBP_OFFSET
    except (TimeoutError, EndPointInternalError, HTTPError, URLError):
        meta["error_counter"] += 1

        if meta["error_counter"] == _ERROR_COUNTER_THRESHOLD:
            console.error(f"{meta['i']}. FAILED: DBpedia query with offset={meta['offset']}")
        else:
            console.warning(f"{meta['i']}. Restoring the connection with offset={meta['offset']}...")

        _write_query_result(meta, file_prefix, mid_path, headers, run_query, _TIMEOUT_SECONDS["ERROR"])
