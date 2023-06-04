import json

from ro.webdata.oniq.endpoint.common.CSVService import CSVService, CSV_COLUMN_SEPARATOR
from ro.webdata.oniq.endpoint.common.path_utils import get_root_path

MATCHED_ENTRIES_FILENAME = "best_matched"
MATCHED_ENTRIES_PATH = get_root_path() + "/files"
MATCHED_ENTRIES_FILEPATH = MATCHED_ENTRIES_PATH + "/" + MATCHED_ENTRIES_FILENAME + ".csv"


class CachedMatch:
    """
    Representation of the result of a similarity check cached on disk.

    Attributes:
        detachment_score (float):
            Aggregated similarity calculated based on the Jaccard Distance
            and Edit Distance.
        prop_uri (str):
            URI of the property that has the highest similarity.
        score (float):
            Similarity score determined by comparing word vectors of the
            target word and the property that has the highest similarity.
        target_word (str):
            Word against the similarity is calculated.

    Methods:
        cache_match(target_word, prop_uri, score, detachment_score, node_type, node_text_value):
            Cache to disk the result of a similarity check.
        get_csv_headers():
            Get the list of column names.
        serialize():
            Serialize the class to a JSON-like string.
        to_csv():
            Prepare the CSV entry.
    """

    def __init__(self, target_word, prop_uri, score, detachment_score, node_type=None, node_text_value=None):
        """
        Args:
            target_word (str):
                Word against the similarity is calculated.
            prop_uri (str):
                URI of the property that has the highest similarity.
            score (str):
                Similarity score determined by comparing word vectors of the
                target word and the property that has the highest similarity.
            detachment_score (str):
                Aggregated similarity calculated based on the Jaccard Distance
                and Edit Distance.
            node_type (str):
                [OPTIONAL] Type of the triple node (NODE_TYPE.OBJECT or NODE_TYPE.SUBJECT).
            node_text_value (str):
                [OPTIONAL] Value of the triple node.
        """

        self.target_word = target_word
        self.prop_uri = prop_uri
        self.score = float(score)
        self.detachment_score = float(detachment_score)
        self.node_type = node_type
        self.node_text_value = node_text_value

    def __hash__(self):
        return hash(self.to_csv())

    def __eq__(self, other):
        # only equality tests to other 'CachedMatch' instances are supported
        if not isinstance(other, CachedMatch):
            return NotImplemented
        return self.to_csv() == other.to_csv()

    def __str__(self):
        return self.to_csv()

    @staticmethod
    def cache_match(target_word, prop_uri, score, detachment_score, node_type=None, node_text_value=None):
        """
        Cache to disk the result of a similarity check.

        Args:
            target_word (str):
                Word against the similarity is calculated.
            prop_uri (str):
                URI of the property that has the highest similarity.
            score (str):
                Similarity score determined by comparing word vectors of the
                target word and the property that has the highest similarity.
            detachment_score (str):
                Aggregated similarity calculated based on the Jaccard Distance
                and Edit Distance.
            node_type (str):
                [OPTIONAL] Type of the triple node (NODE_TYPE.OBJECT or NODE_TYPE.SUBJECT).
            node_text_value (str):
                [OPTIONAL] Value of the triple node.
        """

        matched_entry = CachedMatch(target_word, prop_uri, score, detachment_score, node_type, node_text_value)
        CSVService.append_line(
            MATCHED_ENTRIES_PATH,
            MATCHED_ENTRIES_FILENAME,
            matched_entry.to_csv(),
            CachedMatch.get_csv_headers()
        )

    @staticmethod
    def get_csv_headers():
        """
        Get the list of column names.
        """

        return ['target_word', 'prop_uri', 'score', 'detachment_score', 'node_type', 'node_text_value']

    def serialize(self):
        """
        Serialize the class to a JSON-like string.
        """

        return json.dumps(self.__dict__)

    def to_csv(self, separator=CSV_COLUMN_SEPARATOR):
        """
        Prepare the CSV entry.

        Args:
            separator (str): CSV column separator.

        Returns:
            str: CSV entry.
        """

        return separator.join([
            self.target_word,
            self.prop_uri,
            str(self.score),
            str(self.detachment_score),
            CSVService.to_csv_string(self.node_type),
            CSVService.to_csv_string(self.node_text_value)
        ])
