import spacy
from nltk.corpus import wordnet
from ro.webdata.oniq.model.rdf.SimilarityMap import SimilarityMap
from ro.webdata.oniq.common import rdf_utils

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5', disable=['parser', 'ner'])


class Match:
    def __init__(self, endpoint, verb):
        properties = rdf_utils.get_properties(endpoint)
        similarity_list = _get_similarity_list(verb, properties)
        finest_similarity_score = min(
            similarity_list, key=lambda item: item.similarity
        ).similarity

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
