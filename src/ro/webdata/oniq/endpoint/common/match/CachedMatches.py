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
        [target_word, prop_uri, score, detachment_score, s_uri, o_uri] = csv_entry
        subject_uri = CSVService.get_csv_string(s_uri)
        object_uri = CSVService.get_csv_string(o_uri)

        if not self.exists(target_word, subject_uri, object_uri):
            CachedMatch.cache_match(target_word, prop_uri, score, detachment_score, subject_uri, object_uri)
            matched_entry = CachedMatch(target_word, prop_uri, score, detachment_score, subject_uri, object_uri)

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
            [target_word, prop_uri, score, detachment_score, subject_uri, object_uri] = csv_entry
            matched_entry = CachedMatch(target_word, prop_uri, score, detachment_score, subject_uri, object_uri)
            self.elements.append(matched_entry)

    def append(self, element: CachedMatch):
        """
        Add a new element to the list of cached entries.

        Args:
            element (CachedMatch): New element (CachedMatch).
        """

        self.elements.append(element)

    def exists(self, str_word, subject_uri=None, object_uri=None):
        """
        Check if the target word exists in the input list of cached entries.

        Args:
            str_word (str):
                Target word.
            subject_uri (str):
                [OPTIONAL] The subject to which the property applies.
            object_uri (str):
                [OPTIONAL] The object to which the property applies.

        Returns:
            bool: Validation result.
        """

        for matched_entry in self.elements:
            if matched_entry.target_word == str_word:
                if subject_uri is not None and matched_entry.subject_uri == subject_uri:
                    return True
                if object_uri is not None and matched_entry.object_uri == object_uri:
                    return True

        return False

    def find(self, str_word, subject_uri=None, object_uri=None):
        """
        Find the cached entry corresponding to the target word.

        Args:
            str_word (str):
                Target word.
            subject_uri (str):
                [OPTIONAL] The subject to which the property applies.
            object_uri (str):
                [OPTIONAL] The object to which the property applies.

        Returns:
            CachedMatch:
                The cached entry which contains the target word.
        """

        if self.exists(str_word, subject_uri, object_uri):
            for matched_entry in self.elements:
                if matched_entry.target_word == str_word:
                    if subject_uri is not None and matched_entry.subject_uri == subject_uri:
                        return matched_entry
                    if object_uri is not None and matched_entry.object_uri == object_uri:
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
