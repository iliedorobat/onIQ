import math
import warnings

import nltk
from nltk.corpus import wordnet
from spacy.tokens import Token

from ro.webdata.oniq.common.print_utils import console, SYSTEM_MESSAGES
from ro.webdata.oniq.endpoint.common.CSVService import CSV_COLUMN_SEPARATOR
from ro.webdata.oniq.endpoint.models.RDFElement import RDFProperty
from ro.webdata.oniq.spacy_model import nlp_model

SCORE_BUFFER = 1

# FIXME:
# nlp_model.add_pipe("spacy_wordnet", after='tagger', config={'lang': nlp_model.lang})


class PropertyMatcher:
    """
    Representation of the similarity score calculated for a specific verb
    against an individual property.

    Attributes:
        action (Token):
            Word against the similarity is calculated.
        detachment_score (float):
            Aggregated similarity calculated based on the Jaccard Distance
            and Edit Distance.
        property (RDFProperty):
            Property against which the similarity is calculated.
        result_type (str|None):
            Type of the expected result.
            E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).
        score (float):
            Calculated similarity score.

    Methods:
        to_csv():
            Prepare the CSV entry.
    """

    def __init__(self, rdf_prop, action, result_type):
        """
        Args:
            action (Token):
                Word against the similarity is calculated.
            rdf_prop (RDFProperty):
                Property against which the similarity is calculated.
            result_type (str|None):
                Type of the expected result.
                E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).
        """
        self.action = action
        self.property = rdf_prop
        self.result_type = result_type
        self.score = _calculate_similarity_score(rdf_prop, action, result_type)
        self.detachment_score = _calculate_detachment_score(rdf_prop, action)

    def __hash__(self):
        return hash(f'{self.property.uri}_{self.score}')

    def __eq__(self, other):
        return self.property == other.property and self.score == other.score

    def __str__(self):
        return f'{self.score} => {self.property}'

    def to_csv(self, separator=CSV_COLUMN_SEPARATOR):
        """
        Prepare the CSV entry.

        Args:
            separator (str): CSV column separator.

        Returns:
            str: CSV entry.
        """

        return separator.join([
            self.action,
            self.property.uri,
            str(self.score),
            str(self.detachment_score)
        ])


def _calculate_similarity_score(rdf_prop, action, result_type):
    """
    Determine the similarity between the action and the words that make up
    the label of the property.

    Args:
        action (Token): Word against the similarity is calculated.
        rdf_prop (RDFProperty): Property against which the similarity is
            calculated.
        result_type (str|None):
            Type of the expected result.
            E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).

    Returns:
        float: The score which defines how close the action is to the property.
    """

    return _calculate_word_similarity_score(rdf_prop, action, result_type) + SCORE_BUFFER


def _calculate_word_similarity_score(rdf_prop, word, result_type):
    """
    Determine the similarity between a specific word and the words that
    make up the label of an individual property.

    Args:
        rdf_prop (RDFProperty): Property against which the similarity is
            calculated.
        result_type (str|None):
            Type of the expected result.
            E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).
        word (Token): Token for which the similarity is calculated.

    Returns:
        float: The score which defines how close the property is to word.
    """

    similarity_score = 1
    count = 0

    prop_tokens = rdf_prop.label_to_non_stop_tokens()

    for index, prop_token in list(enumerate(prop_tokens)):
        word_1 = nlp_model(word.text)[0]
        word_2 = nlp_model(prop_token.text)[0]

        if not word_1.has_vector:
            console.warning(SYSTEM_MESSAGES.VECTORS_NOT_AVAILABLE % word_1.text)
        if not word_2.has_vector:
            console.warning(SYSTEM_MESSAGES.VECTORS_NOT_AVAILABLE % word_2.text)

        similarity_score *= (word_1.similarity(word_2) + SCORE_BUFFER)

        # E.g.: birthPlace
        if index > 0 and result_type is not None:
            result_type_token = nlp_model(result_type)[0]

            if not result_type_token.has_vector:
                console.warning(SYSTEM_MESSAGES.VECTORS_NOT_AVAILABLE % result_type_token.text)

            similarity_score *= (word_2.similarity(result_type_token) + SCORE_BUFFER)

        count += 1
        # similarity_list += _get_word_similarity_list(word, non_stop_token, rdf_prop)

    if len(prop_tokens) > 0:
        if similarity_score > 0:
            return math.pow(similarity_score, 1/count) - SCORE_BUFFER
        elif similarity_score < 0:
            return -math.pow(-similarity_score, 1/count) - SCORE_BUFFER

    return 0


def _calculate_detachment_score(rdf_prop, action):
    """
    Determine the similarity between the action and the words that make up
    the label of the property by aggregating the Jaccard Distance and Edit
    Distance metrics.

    Use case:
        - The default similarity value used by <b>spacy</b> generates the
            same result when comparing two antonyms:
            * "successor".similarity("successor") = 1     | good result
            * "successor".similarity("predecessor") = 1   | bad result

    Args:
        action (Token): Word against the similarity is calculated.
        rdf_prop (RDFProperty):
            Property against which the similarity is calculated.

    Returns:
        float:
            Aggregated similarity score.
    """

    prop_name = rdf_prop.name
    action_name = action.text

    jaccard_distance = nltk.jaccard_distance(frozenset(prop_name), frozenset(action_name))
    edit_distance = nltk.edit_distance(prop_name, action_name)

    reversed_jaccard = 1 - jaccard_distance
    # square order "edit_distance + 1" because:
    #   * sqrt(5, 0) = 1.0
    #   * sqrt(5, 1) = 5.0
    #   * sqrt(5, 2) = 2.23606797749979
    reversed_edit = math.pow(len(prop_name), 1/(edit_distance + 1)) / len(prop_name)

    similarity_score = math.pow(reversed_jaccard * reversed_edit, 1/2)

    return similarity_score


def _get_word_similarity_list(lemma: Token, token: Token, rdf_prop: RDFProperty):
    # TODO: remove the method
    warnings.warn("The method is going to be removed", ResourceWarning)

    similarity_list = []
    synonyms = wordnet.synsets(token.text)

    for syn in synonyms:
        for syn_lemma in syn.lemmas():
            syn_name = syn.name().split('.')[0]
            syn_lemma = syn_lemma.name()
            print(f'{syn_name}    {syn_lemma}')
