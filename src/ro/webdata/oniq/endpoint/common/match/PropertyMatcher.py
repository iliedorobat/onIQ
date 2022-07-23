import math
import warnings
from typing import List

from nltk.corpus import wordnet
from spacy.tokens import Token

from ro.webdata.oniq.endpoint.models.RDFElement import RDFProperty
from ro.webdata.oniq.spacy_model import nlp_model

SCORE_BUFFER = 1

nlp_model.add_pipe("spacy_wordnet", after='tagger', config={'lang': nlp_model.lang})


class PropertiesMatcher:
    """
    Representation of the similarity score calculated for a specific action
    (verb) against each property in the target list.

    Attributes:
        matched (List[RDFProperty]):
            List of PropertyMatcher elements representing the properties
            that match the action (verb).

    Methods:
        head():
            Retrieve the property with the highest score from the list of
            matched properties.
    """

    def __init__(self, props, action):
        """
        Args:
            props (List[RDFProperty]): List of properties against which the
                similarity is calculated.
            action (Token): Target verb for which the similarity is calculated.
        """

        self.matched = _get_matched_props(props, action)

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

    def get_best_matched(self):
        """
        Retrieve the PropertyMatcher element containing the property with the
            highest score from the list of matched properties.

        Returns:
            PropertyMatcher: Property having the highest score.
        """

        if len(self.matched) > 0:
            return self.matched[0]
        return None


def _get_matched_props(props, action):
    """
    Determine the similarity between the input verb and the label of each
    property.

    Args:
        action (Token): Verb for which the similarity is calculated.
        props (List[RDFProperty]): List of properties against which the
            similarity is calculated.

    Returns:
        List[PropertyMatcher]: List of PropertyMatcher sorted by highest
            similarity score.
    """

    matched_props = []

    for rdf_prop in props:
        matched_props.append(
            PropertyMatcher(rdf_prop, action)
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
        action (Token): Verb for which the similarity is calculated.
        property (RDFProperty): Property against which the similarity is
            calculated.
        score (float): Calculated similarity score.
    """

    def __init__(self, rdf_prop, action):
        """
        Args:
            action (Token): Verb for which the similarity is calculated.
            rdf_prop (RDFProperty): Property against which the similarity
                is calculated.
        """
        self.action = action
        self.property = rdf_prop
        self.score = _calculate_similarity_score(rdf_prop, action)

    def __hash__(self):
        return hash(f'{self.property.uri}_{self.score}')

    def __eq__(self, other):
        return self.property == other.property and self.score == other.score

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return f'{self.score} => {self.property}'


def _calculate_similarity_score(rdf_prop, action):
    """
    Determine the similarity between the action and the words that make up
    the label of the property.

    Args:
        action (Token): Verb for which the similarity is calculated.
        rdf_prop (RDFProperty): Property against which the similarity is
            calculated.

    Returns:
        float: The score which defines how close the action is to the property.
    """

    return _calculate_word_similarity_score(rdf_prop, action) + SCORE_BUFFER


def _calculate_word_similarity_score(rdf_prop, word):
    """
    Determine the similarity between a specific word and the words that
    make up the label of an individual property.

    Args:
        rdf_prop (RDFProperty): Property against which the similarity is
            calculated.
        word (Token): Token for which the similarity is calculated.

    Returns:
        float: The score which defines how close the property is to word.
    """

    similarity_score = 1
    count = 0

    prop_tokens = rdf_prop.label_to_non_stop_tokens()

    for prop_token in prop_tokens:
        word_1 = nlp_model(word.text)[0]
        word_2 = nlp_model(prop_token.text)[0]
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
