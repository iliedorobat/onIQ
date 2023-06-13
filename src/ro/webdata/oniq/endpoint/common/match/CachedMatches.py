import json
from typing import List

from ro.webdata.oniq.endpoint.common.CSVService import CSVService, CSV_COLUMN_SEPARATOR
from ro.webdata.oniq.endpoint.common.match.CachedMatch import CachedMatch, MATCHED_ENTRIES_FILEPATH


class CachedMatches:
    """
    Representation of the list of cached entries (CachedMatch).

    Attributes:
        elements (List[CachedMatch]):
            List of CachedMatch items.

    Methods:
        append(element):
            Add a new element to the list of cached entries.
        cache_match(csv_line, separator):
            Cache to disk the result of a similarity check and update
            <b>self.elements</b> with the cached result.
        exists(str_word):
            Check if the target word exists in the input list of cached entries.
        find(str_word):
            Find the cached entry corresponding to the target word.
        initialize(separator):
            Initialize <b>self.elements</b> with similarity check entries
            read from <b>MATCHED_ENTRIES_FILEPATH</b>.
        serialize():
            Serialize the class to a JSON-like string.
        sort():
            Sort elements based on property URIs.
        unique():
            Remove duplicates.
    """

    elements: List[CachedMatch]

    def __init__(self, elements: List[CachedMatch] = None):
        """
        Args:
            elements (List[CachedMatch]): Initial list of CachedMatch items.
        """

        if isinstance(elements, list):
            self.elements = elements
        else:
            self.initialize()

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, item):
        return self.elements[item]

    def __str__(self):
        string = ", ".join(
            [str(element) for element in self.elements]
        )

        return f'[{string}]'

    def cache_match(self, csv_line, separator=CSV_COLUMN_SEPARATOR):
        """
        Cache to disk the result of a similarity check and update
        <b>self.elements</b> with the cached result.

        Args:
            csv_line (str): CSV line that will be written to disk.
            separator (str): CSV column separator.
        """

        csv_entry = csv_line.strip().split(separator)
        [target_word, prop_uri, score, detachment_score, raw_target_type, raw_target_value] = csv_entry
        node_type = CSVService.get_csv_string(raw_target_type)
        node_text_value = CSVService.get_csv_string(raw_target_value)

        if not self.exists(target_word, node_type, node_text_value):
            CachedMatch.cache_match(target_word, prop_uri, score, detachment_score, node_type, node_text_value)
            matched_entry = CachedMatch(target_word, prop_uri, score, detachment_score, node_type, node_text_value)

            self.elements.append(matched_entry)

    def initialize(self, separator=CSV_COLUMN_SEPARATOR):
        """
        Initialize <b>self.elements</b> with similarity check entries
        read from <b>MATCHED_ENTRIES_FILEPATH</b>.

        Args:
            separator (str): CSV column separator.
        """

        self.elements = []

        for csv_line in CSVService.read_lines(MATCHED_ENTRIES_FILEPATH, True):
            csv_entry = csv_line.strip().split(separator)
            [target_word, prop_uri, score, detachment_score, node_type, node_text_value] = csv_entry
            matched_entry = CachedMatch(
                target_word,
                prop_uri,
                score,
                detachment_score,
                CSVService.get_csv_string(node_type),
                CSVService.get_csv_string(node_text_value)
            )
            self.elements.append(matched_entry)

    def append(self, element: CachedMatch):
        """
        Add a new element to the list of cached entries.

        Args:
            element (CachedMatch): New element (CachedMatch).
        """

        self.elements.append(element)

    def exists(self, str_word, node_type=None, node_text_value=None):
        """
        Check if the target word exists in the input list of cached entries.

        Args:
            str_word (str):
                Target word.
            node_type (str):
                [OPTIONAL] Type of the triple node (NODE_TYPE.OBJECT or NODE_TYPE.SUBJECT).
            node_text_value (str):
                [OPTIONAL] Value of the triple node.

        Returns:
            bool: Validation result.
        """

        for matched_entry in self.elements:
            if matched_entry.target_word == str_word:
                if matched_entry.node_type == node_type:
                    if matched_entry.node_text_value == node_text_value:
                        return True

        return False

    def find(self, str_word, node_type=None, node_text_value=None):
        """
        Find the cached entry corresponding to the target word.

        Args:
            str_word (str):
                Target word.
            node_type (str):
                [OPTIONAL] Type of the triple node (NODE_TYPE.OBJECT or NODE_TYPE.SUBJECT).
            node_text_value (str):
                [OPTIONAL] Value of the triple node.

        Returns:
            CachedMatch:
                The cached entry which contains the target word.
        """

        if self.exists(str_word, node_type, node_text_value):
            for matched_entry in self.elements:
                if matched_entry.target_word == str_word:
                    if matched_entry.node_type == node_type:
                        if matched_entry.node_text_value == node_text_value:
                            return matched_entry

        return None

    def serialize(self):
        """
        Serialize the class to a JSON-like string.
        """

        return json.dumps(self.__dict__)

    def sort(self):
        """
        Sort elements based on property URIs.
        """

        self.elements = sorted(self.elements, key=lambda item: item.prop_uri)

    def unique(self):
        """
        Remove duplicates.
        """

        self.elements = list(set(self.elements))
