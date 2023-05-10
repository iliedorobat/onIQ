from typing import Union

from nltk.corpus import wordnet as wn
from spacy.tokens import Doc, Span


def is_doc_or_span(phrase: Union[Doc, Span]):
    """
    Determine if the input phrase is an instance of Doc or Span.

    :param phrase:
    :return: True/False
    """

    return isinstance(phrase, Doc) or isinstance(phrase, Span)


def is_empty_list(input_list: list):
    """
    Determine if the input list is empty or not.

    :param input_list: The target list.
    :return: True/False
    """

    return not isinstance(input_list, list) or len(input_list) == 0


class WordnetUtils:
    WN_NOUN = 'n'
    WN_VERB = 'v'
    WN_ADJECTIVE = 'a'
    WN_ADJECTIVE_SATELLITE = 's'
    WN_ADVERB = 'r'

    @staticmethod
    def convert(word, from_pos, to_pos):
        """
        Transform words given from/to POS tags.

        SOURCE: https://stackoverflow.com/questions/14489309/convert-words-between-verb-noun-adjective-forms
        """
    
        # E.g.: convert("swedish", "a", "n")
        # E.g.: convert('direct', 'a', 'n')
    
        synsets = wn.synsets(word, pos=from_pos)
    
        # Word not found
        if not synsets:
            return []
    
        # Get all lemmas of the word (consider 'a'and 's' equivalent)
        lemmas = [l for s in synsets
                  for l in s.lemmas()
                  if s.name().split('.')[1] == from_pos
                  or from_pos in (WordnetUtils.WN_ADJECTIVE, WordnetUtils.WN_ADJECTIVE_SATELLITE)
                  and s.name().split('.')[1] in (WordnetUtils.WN_ADJECTIVE, WordnetUtils.WN_ADJECTIVE_SATELLITE)]
    
        # Get related forms
        derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]
    
        # filter only the desired pos (consider 'a' and 's' equivalent)
        related_noun_lemmas = [l for drf in derivationally_related_forms
                               for l in drf[1]
                               if l.synset().name().split('.')[1] == to_pos
                               or to_pos in (WordnetUtils.WN_ADJECTIVE, WordnetUtils.WN_ADJECTIVE_SATELLITE)
                               and l.synset().name().split('.')[1] in (WordnetUtils.WN_ADJECTIVE, WordnetUtils.WN_ADJECTIVE_SATELLITE)]
    
        # Extract the words from the lemmas
        words = [l.name() for l in related_noun_lemmas]
        len_words = len(words)
    
        # Build the result in the form of a list containing tuples (word, probability)
        result = [(w, float(words.count(w))/len_words) for w in set(words)]
        result.sort(key=lambda w: -w[1])
    
        # return all the possibilities sorted by probability
        return result

    @staticmethod
    def find_country_by_nationality(nationality):
        """
        Finds the name of the country given a nationality.

        SOURCE: https://gist.github.com/filipelm/bb3b1387071c5b84a5b5f5baf20aa925

        :param nationality: The nationality (ie. Irish).
        :return: The country name.
        """

        return wn.lemmas(nationality, pos=wn.ADJ)[0].pertainyms()[0]._name
