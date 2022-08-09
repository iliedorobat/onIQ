import warnings

from nltk.corpus import wordnet

from ro.webdata.oniq.model.rdf.Property import Property
from ro.webdata.oniq.model.rdf.SimilarityMap import SimilarityMap


class Match:

    warnings.warn("deprecated in favour of PropertyMatcher", DeprecationWarning)

    def __init__(self, rdf_props: [Property], words: [str]):
        similarity_list = _get_similarity_list(words, rdf_props)
        finest_similarity_score = _get_similarity_score(similarity_list)

        # list of distinct property names which have the finest similarity scores
        self.matched = set(
            [
                similarityMap.prop_name for similarityMap in list(
                    filter(
                        lambda item: item.similarity == finest_similarity_score, similarity_list
                    )
                )
            ]
        )

    def __str__(self):
        output = f'match size: {len(self.matched)}\n'
        for prop_name in self.matched:
            output += f'prop_name: {prop_name}\n'
        return output


def _get_similarity_score(similarity_list):
    if len(similarity_list) == 0:
        return 0

    return min(
        similarity_list, key=lambda item: item.similarity
    ).similarity


def _get_similarity_list(words, properties):
    similarity_list = []

    for word in words:
        similarity_list += _get_word_similarity_list(word, properties)

    return similarity_list


def _get_word_similarity_list(word, properties):
    similarity_list = []
    synonyms = wordnet.synsets(word)

    for prop in properties:
        prop_name = prop.prop_name
        prop_lemma = prop.lemma

        # E.g.: "wasPresentAt"
        if prop_name == word:
            similarity_list.append(
                SimilarityMap(
                    prop_name, prop_lemma, prop_name, prop_lemma
                )
            )

        for syn in synonyms:
            for lemma in syn.lemmas():
                syn_name = syn.name().split('.')[0]
                syn_lemma = lemma.name()

                similarity_list.append(
                    SimilarityMap(
                        prop_name, prop_lemma, syn_name, syn_lemma
                    )
                )

    return similarity_list
