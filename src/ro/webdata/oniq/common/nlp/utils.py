from typing import Union

import pydash
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
from spacy.tokens import Doc, Span


class SENTI_WORD_TYPE:
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"


def get_resource_name(entity_span: Span):
    resource_uri = entity_span.kb_id_
    namespace = get_resource_namespace(entity_span)

    return resource_uri.replace(namespace, "")


def get_resource_namespace(entity_span: Span):
    resource_uri = entity_span.kb_id_

    last_index = resource_uri.rfind("/") + 1
    if last_index == -1:
        last_index = resource_uri.rfind("#") + 1

    return resource_uri[0: last_index]


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

        lemmas = wn.lemmas(nationality, pos=wn.ADJ)
        lemma = pydash.get(lemmas, "0")

        try:
            pertainyms = lemma.pertainyms()
            pertainym = pydash.get(pertainyms, "0")

            return pydash.get(pertainym, "_name")
        except AttributeError:
            # E.g.: "Who is the youngest Pulitzer Prize winner?"
            return None

    @staticmethod
    def senti_word_analysis(word: str):
        if isinstance(word, str):
            sent_list = list(swn.senti_synsets(word, 'a'))
            sent_item = pydash.get(sent_list, "0")

            if sent_item is not None and sent_item.synset.definition() == "greater than normal in degree or intensity or amount":
                # E.g.: "What is the highest mountain in the Bavarian Alps?"
                sent_item = sent_item = pydash.get(sent_list, "1")

            pos_score = sent_item.pos_score()
            neg_score = sent_item.neg_score()

            if neg_score > pos_score:
                return SENTI_WORD_TYPE.NEGATIVE
            elif neg_score == pos_score:
                return SENTI_WORD_TYPE.NEUTRAL
            else:
                return SENTI_WORD_TYPE.POSITIVE

        return None
