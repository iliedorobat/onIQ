import nltk
import spacy

from nltk.corpus import wordnet

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5', disable=['parser', 'ner'])


class Match:
    def __init__(self, verb, properties):
        similarity_list = _get_similarity_list(verb, properties)
        finest_similarity = min(
            similarity_list, key=lambda item: item.similarity
        ).similarity
        self.matched = list(
            filter(
                lambda item: item.similarity == finest_similarity, similarity_list
            )
        )

    def __str__(self):
        output = f'match size: {len(self.matched)}\n'
        for item in self.matched:
            output += str(item) + "\n"
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
    for item in CUSTOM_FIT:
        if (prop_name == item["prop_name"] and syn_name == item["syn_name"]) or \
                (prop_name == item["syn_name"] and syn_name == item["prop_name"]):
            return 0

    return nltk.jaccard_distance(
        frozenset(prop_lemma), frozenset(syn_lemma)
    )


def _get_similarity_list(verb, properties):
    similarity_list = []
    synonyms = wordnet.synsets(verb)

    for prop in properties:
        for syn in synonyms:
            for lemma in syn.lemmas():
                prop_name = prop.prop_name
                prop_lemma = prop.lemma.prop_name
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
