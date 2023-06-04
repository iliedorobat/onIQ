import math
import warnings

import nltk
from nltk.corpus import wordnet
from spacy.tokens import Token

from ro.webdata.oniq.common.print_utils import console, SYSTEM_MESSAGES
from ro.webdata.oniq.endpoint.common.CSVService import CSV_COLUMN_SEPARATOR
from ro.webdata.oniq.endpoint.models.RDFElement import RDFProperty
from ro.webdata.oniq.spacy_model import nlp_model
from ro.webdata.oniq.sparql.constants import SPARQL_STR_SEPARATOR

SCORE_BUFFER = 1

# FIXME:
# nlp_model.add_pipe("spacy_wordnet", after='tagger', config={'lang': nlp_model.lang})


class PropertyMatcher:
    """
    Representation of the similarity score calculated for a specific word
    or sequences of words (an expression) against an individual property.

    Attributes:
        target_expression (Span):
            Word/expression against the similarity is calculated.
        detachment_score (float):
            Aggregated similarity calculated based on the Jaccard Distance
            and Edit Distance.
        object_uri (str):
            The object to which the property applies.
        property (RDFProperty):
            Property against which the similarity is calculated.
        result_type (str|None):
            Type of the expected result.
            E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).
        score (float):
            Calculated similarity score.
        subject_uri (str):
            The subject to which the property applies.

    Methods:
        to_csv():
            Prepare the CSV entry.
    """

    def __init__(self, rdf_prop, target_expression, result_type, subject_uri, object_uri):
        """
        Args:
            target_expression (Span):
                Word/expression against the similarity is calculated.
            rdf_prop (RDFProperty):
                Property against which the similarity is calculated.
            result_type (str|None):
                Type of the expected result.
                E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).
            subject_uri (str):
                [OPTIONAL] The subject to which the property applies.
            object_uri (str):
                [OPTIONAL] The object to which the property applies.
        """

        self.target_expression = target_expression
        self.property = rdf_prop
        self.result_type = result_type
        self.score = _calculate_similarity_score(rdf_prop, target_expression, result_type)
        self.detachment_score = _calculate_detachment_score(rdf_prop, target_expression)
        self.subject_uri = subject_uri
        self.object_uri = object_uri

    def __hash__(self):
        return hash(f'{self.property.uri}{SPARQL_STR_SEPARATOR}{self.score}')

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

        subject_uri = self.subject_uri if self.subject_uri is not None else ""
        object_uri = self.object_uri if self.object_uri is not None else ""

        return separator.join([
            self.target_expression.text,
            self.property.uri,
            str(self.score),
            str(self.detachment_score),
            subject_uri,
            object_uri
        ])


def _calculate_similarity_score(rdf_prop, target_expression, result_type):
    """
    Determine the similarity between the target word/expression and the words
    that make up the label of the property.

    Args:
        target_expression (Span): Word/expression against the similarity
            is calculated.
        rdf_prop (RDFProperty): Property against which the similarity is
            calculated.
        result_type (str|None):
            Type of the expected result.
            E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).

    Returns:
        float: The score which defines how close the target word/expression
            is to the property.
    """

    return _calculate_word_similarity_score(rdf_prop, target_expression, result_type) + SCORE_BUFFER


def _calculate_word_similarity_score(rdf_prop, target_expression, result_type):
    """
    Determine the similarity between a specific word and the words that
    make up the label of an individual property.

    Args:
        rdf_prop (RDFProperty): Property against which the similarity is
            calculated.
        result_type (str|None):
            Type of the expected result.
            E.g.: "place", "person", etc. (check DBPEDIA_CLASS_TYPES).
        target_expression (Span): Word/expression against the similarity
            is calculated.

    Returns:
        float: The score which defines how close the property is to word.
    """

    similarity_score = 1
    count = 0

    prop_tokens = rdf_prop.label_to_non_stop_tokens()

    for index, prop_token in list(enumerate(prop_tokens)):
        # FIXME: workaround for "born".lemma_ == "bear"
        workaround_word_1 = "birth" if target_expression.text == "born" else target_expression.lemma_

        word_1 = nlp_model(workaround_word_1)[0]
        word_2 = nlp_model(prop_token.lemma_)[0]

        if not word_1.has_vector:
            console.warning(SYSTEM_MESSAGES.VECTORS_NOT_AVAILABLE % word_1.lemma_)
        if not word_2.has_vector:
            console.warning(SYSTEM_MESSAGES.VECTORS_NOT_AVAILABLE % word_2.lemma_)

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


def _calculate_detachment_score(rdf_prop, target_expression):
    """
    Determine the similarity between the target word/expression and the words
    that make up the label of the property by aggregating the Jaccard Distance
    and Edit Distance metrics.

    Use case:
        - The default similarity value used by <b>spacy</b> generates the
            same result when comparing two antonyms:
            * "successor".similarity("successor") = 1     | good result
            * "successor".similarity("predecessor") = 1   | bad result

    Args:
        target_expression (Span):
            Word/expression against the similarity is calculated.
        rdf_prop (RDFProperty):
            Property against which the similarity is calculated.

    Returns:
        float:
            Aggregated similarity score.
    """

    prop_name = rdf_prop.name
    target_text = target_expression.text

    jaccard_distance = nltk.jaccard_distance(frozenset(prop_name), frozenset(target_text))
    edit_distance = nltk.edit_distance(prop_name, target_text)

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
