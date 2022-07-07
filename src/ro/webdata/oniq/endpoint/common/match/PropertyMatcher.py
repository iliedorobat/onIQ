import math
import warnings
from typing import List

import spacy
from nltk.corpus import wordnet
from spacy.tokens import Token

from ro.webdata.oniq.endpoint.models.RDFElement import RDFProperty
from ro.webdata.oniq.model.sentence.Verb import Verb

nlp = spacy.load('en_core_web_md')
SCORE_BUFFER = 1


class PropertiesMatcher:
    """
    Representation of the similarity score calculated for a specific verb
    (type of Verb) against each property in the target list.

    Attributes:
        matched (List[RDFProperty]):
            List of PropertyMatcher elements representing the properties
            that match the verb.

    Methods:
        head():
            Retrieve the property with the highest score from the list of
            matched properties.
    """

    def __init__(self, verb, props):
        """
        Args:
            verb (Verb): Target verb for which the similarity is calculated.
            props (List[RDFProperty]): List of properties against which the
                similarity is calculated.
        """
        self.matched = _get_matched_props(verb, props)

    def __hash__(self):
        hash_value = ""

        for item in self.matched:
            hash_value += f'{item.property.uri}_{item.score}'

        return hash(hash_value)

    def __eq__(self, others):
        if len(self.matched) != len(others.matched):
            return False

        for item in self.matched:
            exists = item in others.matched

            if not exists:
                return False

        return True

    def head(self):
        """
        Retrieve the PropertyMatcher element containing the property with the
            highest score from the list of matched properties.

        Returns:
            PropertyMatcher: Property with the highest score.
        """

        if len(self.matched) > 0:
            return self.matched[0]
        return None


def _get_matched_props(verb, props):
    """
    Determine the similarity between the input verb and the label of each
    property.

    Args:
        verb (Verb): Verb for which the similarity is calculated.
        props (List[RDFProperty]): List of properties against which the
            similarity is calculated.

    Returns:
        List[PropertyMatcher]: List of PropertyMatcher sorted by highest
            similarity score.
    """

    matched_props = []

    for rdf_prop in props:
        matched_props.append(
            PropertyMatcher(verb, rdf_prop)
        )

    return sorted(
        matched_props,
        key=lambda match: match.score,
        reverse=True
    )


class PropertyMatcher:
    """
    Representation of the similarity score calculated for a specific verb
    against an individual property.

    Attributes:
        verb (Verb): Verb for which the similarity is calculated.
        property (RDFProperty): Property against which the similarity is
            calculated.
        score (float): Calculated similarity score.
    """

    def __init__(self, verb, rdf_prop):
        """
        Args:
            verb (Verb): Verb for which the similarity is calculated.
            rdf_prop (RDFProperty): Property against which the similarity
                is calculated.
        """
        self.verb = verb
        self.property = rdf_prop
        self.score = _calculate_verbs_similarity_score(verb, rdf_prop)

    def __hash__(self):
        return hash(f'{self.property.uri}_{self.score}')

    def __eq__(self, other):
        return self.property == other.property and self.score == other.score

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return f'{self.score} => {self.property}'


def _calculate_verbs_similarity_score(verb, rdf_prop):
    """
    Determine the similarity between the list of lexical verbs (a Verb
    consists in a list of auxiliary verbs, modal verbs and main verb) and
    the words that make up the label of the property.

    Args:
        verb (Verb): Verb for which the similarity is calculated.
        rdf_prop (RDFProperty): Property against which the similarity is
            calculated.

    Returns:
        float: The score which defines how close the list of lexical verbs
            is to the property.
    """

    similarity_score = 1
    count = 0

    verb_tokens = verb.to_non_stop_list()

    for token in verb_tokens:
        similarity_score *= (_calculate_word_similarity_score(token, rdf_prop) + SCORE_BUFFER)
        count += 1

    if len(verb_tokens) > 0:
        if similarity_score > 0:
            return math.pow(similarity_score, 1/count) - SCORE_BUFFER
        elif similarity_score < 0:
            return -math.pow(-similarity_score, 1/count) - SCORE_BUFFER

    return 0


def _calculate_word_similarity_score(word, rdf_prop):
    """
    Determine the similarity between a specific word and the words that
    make up the label of an individual property.

    Args:
        word (Token): Token for which the similarity is calculated.
        rdf_prop (RDFProperty): Property against which the similarity is
            calculated.

    Returns:
        float: The score which defines how close the property is to word.
    """

    similarity_score = 1
    count = 0

    prop_tokens = rdf_prop.label_to_non_stop_tokens()

    for prop_token in prop_tokens:
        word_1 = nlp(word.text)[0]
        word_2 = nlp(prop_token.text)[0]
        similarity_score *= (word_1.similarity(word_2) + SCORE_BUFFER)
        count += 1
        # similarity_list += _get_word_similarity_list(word, non_stop_token, rdf_prop)

    if len(prop_tokens) > 0:
        if similarity_score > 0:
            return math.pow(similarity_score, 1/count) - SCORE_BUFFER
        elif similarity_score < 0:
            return -math.pow(-similarity_score, 1/count) - SCORE_BUFFER

    return 0


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
