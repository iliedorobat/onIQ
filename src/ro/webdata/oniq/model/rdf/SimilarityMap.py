import math
import warnings

import nltk

from ro.webdata.oniq.common.print_utils import console


class SimilarityMap:
    warnings.warn("Deprecated in favour or PropertyMatcher", PendingDeprecationWarning)

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
    # TODO: customize the matching mechanism
    for item in CUSTOM_FIT:
        if (prop_name == item["prop_name"] and syn_name == item["syn_name"]) or \
                (prop_name == item["syn_name"] and syn_name == item["prop_name"]):
            return 0

    jaccard_distance = nltk.jaccard_distance(frozenset(prop_lemma), frozenset(syn_lemma))
    edit_distance = nltk.edit_distance(prop_lemma, syn_lemma)
    root_edit_distance = math.pow(edit_distance, 1/len(prop_lemma))
    similarity_score = math.pow(jaccard_distance * root_edit_distance, 1/2)

    console.extra_debug(f'sim: {prop_name},   {prop_lemma},   {syn_name},   {syn_lemma},'
                        f'   {similarity_score},   {jaccard_distance},   {edit_distance}')

    return similarity_score


CUSTOM_FIT = [
    {"prop_name": "subject", "syn_name": "category"}
]
