import math
import nltk
import spacy

from nltk.corpus import wordnet
from ro.webdata.oniq.rdf import parser

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5', disable=['parser', 'ner'])


class Match:
    def __init__(self, endpoint, verb):
        properties = parser.get_properties(endpoint)
        similarity_list = _get_similarity_list(verb, properties)
        finest_similarity_score = min(
            similarity_list, key=lambda item: item.similarity
        ).similarity

        # list of distinct properties name which have the finest similarity score
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


class SimilarityMap:
    def __init__(self, prop_name, prop_lemma, syn_name, syn_lemma):
        self.prop_name = prop_name
        self.prop_lemma = prop_lemma
        self.syn_name = syn_name
        self.syn_lemma = syn_lemma
        self.similarity = _get_similarity_score(prop_name, prop_lemma, syn_name, syn_lemma)

    def __str__(self):
        return f'prop_name: {self.prop_name:{10}} ' \
               f'prop_lemma: {self.prop_lemma:{10}} ' \
               f'syn_name: {self.syn_name:{10}} ' \
               f'syn_lemma: {self.syn_lemma:{10}} ' \
               f'similarity: {self.similarity:{5}}'


def _get_similarity_score(prop_name, prop_lemma, syn_name, syn_lemma):
    # TODO: customizable fit
    for item in CUSTOM_FIT:
        if (prop_name == item["prop_name"] and syn_name == item["syn_name"]) or \
                (prop_name == item["syn_name"] and syn_name == item["prop_name"]):
            return 0

    jaccard_distance = nltk.jaccard_distance(frozenset(prop_lemma), frozenset(syn_lemma))
    edit_distance = nltk.edit_distance(prop_lemma, syn_lemma)
    root_edit_distance = math.pow(edit_distance, 1/len(prop_lemma))
    similarity_score = math.pow(jaccard_distance * root_edit_distance, 1/2)

    print('sim:', prop_name, '   ', prop_lemma, '    ', syn_name, '    ', syn_lemma, '  ', similarity_score, jaccard_distance, edit_distance)

    return similarity_score


def _get_similarity_list(verb, properties):
    similarity_list = []
    synonyms = wordnet.synsets(verb)

    for prop in properties:
        for syn in synonyms:
            for lemma in syn.lemmas():
                prop_name = prop.prop_name
                prop_lemma = prop.lemma
                syn_name = syn.name().split('.')[0]
                syn_lemma = lemma.name()

                similarity_list.append(
                    SimilarityMap(
                        prop_name, prop_lemma, syn_name, syn_lemma
                    )
                )

    return similarity_list


CUSTOM_FIT = [
    {"prop_name": "subject", "syn_name": "category"}
]
