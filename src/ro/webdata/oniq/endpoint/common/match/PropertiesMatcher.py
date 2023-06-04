from typing import List

import pydash

from ro.webdata.oniq.endpoint.common.match.CachedMatches import CachedMatches
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.sparql.constants import SPARQL_STR_SEPARATOR

CACHED_MATCHES = CachedMatches()


class PropertiesMatcher:
    """
    Representation of the similarity score calculated for a specific word or
    sequences of words (an expression) against each property in the property list.

    Attributes:
        matches (RDFElements[RDFProperty]):
            List of PropertyMatcher elements representing the properties
            that match the target word/expression.

    Methods:
        get_best_matched(props, target_expression, result_type):
            Retrieve the PropertyMatcher element containing the property with the
            highest score from the list of matched properties.
    """

    def __init__(self, props, target_expression, result_type=None, subject_uri=None, object_uri=None):
        """
        Args:
            props (List[RDFProperty]):
                List of properties against which the similarity is calculated.
            target_expression (Span):
                Word/expression for which the similarity is calculated.
            result_type (str|None):
                [OPTIONAL] Type of the expected result.
                E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).
            subject_uri (str):
                [OPTIONAL] The subject to which the property applies.
            object_uri (str):
                [OPTIONAL] The object to which the property applies.
        """

        self.matches = _get_matched_props(props, target_expression, result_type, subject_uri, object_uri)

    def __hash__(self):
        hash_value = "##".join(
            [f'{item.property.uri}{SPARQL_STR_SEPARATOR}{item.score}' for item in self.matches]
        )

        return hash(hash_value)

    def __eq__(self, others):
        if len(self.matches) != len(others.matched):
            return False

        for item in self.matches:
            exists = item in others.matched

            if not exists:
                return False

        return True

    @staticmethod
    def get_best_matched(props, target_expression, result_type=None, subject_uri=None, object_uri=None):
        """
        Retrieve the PropertyMatcher element containing the property with the
        highest score from the list of matched properties.

        Args:
            props (RDFElements[RDFProperty]):
                List of properties against which the similarity is calculated.
            target_expression (Span):
                Word/expression for which the similarity is calculated.
            result_type (str|None):
                [OPTIONAL] Type of the expected result.
                E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).
            subject_uri (str):
                [OPTIONAL] The subject to which the property applies.
            object_uri (str):
                [OPTIONAL] The object to which the property applies.

        Returns:
            PropertyMatcher: Property having the highest score.
        """

        # Get <b>best matched</b> from disk if it has already been cached.
        if CACHED_MATCHES.exists(target_expression.text, subject_uri, object_uri):
            matched = CACHED_MATCHES.find(target_expression.text, subject_uri, object_uri)
            rdf_prop = props.find(matched.prop_uri)
            best_match = PropertyMatcher(rdf_prop, target_expression, result_type, subject_uri, object_uri)

            return best_match

        matcher = PropertiesMatcher(props, target_expression, result_type, subject_uri, object_uri)
        matches = matcher.matches
        best_match = pydash.get(matcher.matches, '0')

        if len(matches) > 0:
            best_score = best_match.score
            best_matches = [item for item in matches if item.score == best_score]

            # E.g.: spacy: "successor".similarity("successor") = 1
            # E.g.: spacy: "successor".similarity("predecessor") = 1
            if len(best_matches) > 0:
                best_matches = sorted(
                    best_matches,
                    key=lambda match: match.detachment_score,
                    reverse=True
                )
                best_match = best_matches[0]

            CACHED_MATCHES.cache_match(best_match.to_csv())

        return best_match


def _get_matched_props(props, target_expression, result_type=None, subject_uri=None, object_uri=None):
    """
    Determine the similarity between the input verb and the label of each
    property.

    Args:
        props (RDFElements[RDFProperty]):
            List of properties against which the similarity is calculated.
        target_expression (Span):
            Word/expression for which the similarity is calculated.
        result_type (str|None):
            [OPTIONAL] Type of the expected result.
            E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).
        subject_uri (str):
            [OPTIONAL] The subject to which the property applies.
        object_uri (str):
            [OPTIONAL] The object to which the property applies.

    Returns:
        List[PropertyMatcher]:
            List of PropertyMatcher sorted by highest similarity score.
    """

    matched_props = [
        PropertyMatcher(rdf_prop, target_expression, result_type, subject_uri, object_uri)
        for rdf_prop in props
    ]

    return sorted(
        matched_props,
        key=lambda match: match.score,
        reverse=True
    )
