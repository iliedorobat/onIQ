from typing import List

import pydash

from ro.webdata.oniq.endpoint.common.match.CachedMatches import CachedMatches
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher

CACHED_MATCHES = CachedMatches()


class PropertiesMatcher:
    """
    Representation of the similarity score calculated for a specific action
    (verb) against each property in the target list.

    Attributes:
        matches (RDFElements[RDFProperty]):
            List of PropertyMatcher elements representing the properties
            that match the action (verb).

    Methods:
        get_best_matched(props, action, result_type):
            Retrieve the PropertyMatcher element containing the property with the
            highest score from the list of matched properties.
    """

    def __init__(self, props, action, result_type):
        """
        Args:
            props (List[RDFProperty]):
                List of properties against which the similarity is calculated.
            action (Token):
                Target verb for which the similarity is calculated.
            result_type (str|None):
                Type of the expected result.
                E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).
        """

        self.matches = _get_matched_props(props, action, result_type)

    def __hash__(self):
        hash_value = "##".join(
            [f'{item.property.uri}_{item.score}' for item in self.matches]
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
    def get_best_matched(props, action, result_type):
        """
        Retrieve the PropertyMatcher element containing the property with the
        highest score from the list of matched properties.

        Args:
            props (RDFElements[RDFProperty]):
                List of properties against which the similarity is calculated.
            action (Token):
                Target verb for which the similarity is calculated.
            result_type (str|None):
                Type of the expected result.
                E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).

        Returns:
            PropertyMatcher: Property having the highest score.
        """

        # Get <b>best matched</b> from disk if it has already been cached.
        if CACHED_MATCHES.exists(action.text):
            matched = CACHED_MATCHES.find(action.text)
            rdf_prop = props.find(matched.prop_uri)
            best_match = PropertyMatcher(rdf_prop, action, result_type)

            return best_match

        matcher = PropertiesMatcher(props, action, result_type)
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


def _get_matched_props(props, action, result_type):
    """
    Determine the similarity between the input verb and the label of each
    property.

    Args:
        action (Token):
            Word against the similarity is calculated.
        props (List[RDFProperty]):
            List of properties against which the similarity is calculated.

    Returns:
        List[PropertyMatcher]:
            List of PropertyMatcher sorted by highest similarity score.
    """

    matched_props = [
        PropertyMatcher(rdf_prop, action, result_type)
        for rdf_prop in props
    ]

    return sorted(
        matched_props,
        key=lambda match: match.score,
        reverse=True
    )
