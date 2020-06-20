import nltk
import spacy

from nltk.corpus import wordnet

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5', disable=['parser', 'ner'])


class Match:
    def __init__(self, prop_name, properties):
        similarity_list = _get_similarity_list(prop_name, properties)
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
    def __init__(self, syn_lemma, prop_lemma):
        self.syn_lemma = syn_lemma
        self.prop_lemma = prop_lemma
        self.similarity = nltk.jaccard_distance(
            frozenset(prop_lemma), frozenset(syn_lemma)
        )

    def __str__(self):
        return f'syn_lemma: {self.syn_lemma:{10}}' \
               f'prop_lemma: {self.prop_lemma:{10}}' \
               f'similarity: {self.similarity:{5}}'


def _get_similarity_list(prop_name, properties):
    similarity_list = []
    synonyms = wordnet.synsets(prop_name)

    for prop in properties:
        for syn in synonyms:
            for lemma in syn.lemmas():
                prop_lemma = prop.lemma.prop_name
                similarity_map = SimilarityMap(lemma.name(), prop_lemma)
                similarity_list.append(similarity_map)

    return similarity_list
