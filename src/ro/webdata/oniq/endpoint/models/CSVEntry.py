import re
from typing import List
from urllib.parse import unquote

from ro.webdata.oniq.common.text_utils import WORD_SEPARATOR
from ro.webdata.oniq.endpoint.common.CSVService import CSV_COLUMN_SEPARATOR, CSV_VALUE_SEPARATOR


class CSVEntry:
    """
    Representation a line read from a CSV file.

    Attributes:
        namespace (str):
            Namespace of the resource.
        namespace_label (str):
            Label of the namespace of the resource.
        parent_uris (List[str]):
            List of parent resource URIs.
        resource_label (str):
            Label of the resource.
        resource_uri (str):
            URI of the resource.
    """

    def __init__(self, csv_line, extract_label=False, separator=CSV_COLUMN_SEPARATOR):
        """
        Args:
            csv_line (str): Content of a line read from a CSV file.
            extract_label (bool): Specify if "_extract_resource_label" method
                will be used or not to get the resource's label.
            separator (str): CSV column separator.
        """

        csv_entry = csv_line.strip().split(separator)

        self.namespace = csv_entry[2]
        self.namespace_label = csv_entry[0]
        self.parent_uris = csv_entry[4].split(CSV_VALUE_SEPARATOR) \
            if csv_entry[4] is not None and len(csv_entry[4]) > 0 \
            else []
        self.resource_uri = csv_entry[3]
        self.resource_label = _extract_resource_label(self.resource_uri, self.namespace) \
            if extract_label \
            else csv_entry[1]
        self.res_domain = csv_entry[5] if len(csv_entry) > 5 else None
        self.res_range = csv_entry[6] if len(csv_entry) > 6 else None


def _extract_resource_label(resource_uri, namespace):
    """
    Extract the resource label from its URI.

    Args:
        resource_uri (str): Resource URI.
        namespace (str): Resource namespace.

    Returns:
        str: Resource's label.
    """

    unquoted = unquote(
        resource_uri.replace(namespace, "")
    )
    word_separator = WORD_SEPARATOR
    word_list = re.sub("[^0-9a-zA-Z\"\']+", word_separator, unquoted).split(word_separator)
    word_list = [
        word.strip()
        for word in word_list
    ]
    word_list = list(
        filter(
            lambda word: len(word) > 0, word_list
        )
    )

    return word_separator.join(word_list)
