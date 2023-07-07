from typing import List

from spacy.tokens import Token

from ro.webdata.oniq.common.nlp.utils import WordnetUtils
from ro.webdata.oniq.common.nlp.word_utils import is_preposition, is_noun, is_adj, get_next_word
from ro.webdata.oniq.sparql.NLQuestion import NLQuestion, QUESTION_TYPES
from ro.webdata.oniq.sparql.NounEntity import NounEntity


class TokenHandler:
    @staticmethod
    def adj_not_found(noun: Token, adjective: Token):
        adjective_cond = True
        country_cond = True

        if is_noun(noun):
            country = WordnetUtils.find_country_by_nationality(adjective.text)

            if country is None:
                # E.g.: "What is the net income of Apple?"
                # E.g.: "How high is the Yokohama Marine Tower?"
                adjective_cond = adjective.lower_ not in NounEntity(noun).to_span().text.lower()
            else:
                # E.g.: "Give me all Swedish holidays." => country is not None
                country_cond = country.lower() not in NounEntity(noun).to_span().text.lower()

        return country_cond and adjective_cond

    @staticmethod
    def noun_not_found(noun: Token, head: Token):
        if is_noun(noun):
            # E.g.: "Who is the youngest Pulitzer Prize winner?"
            head_is_attr = head.dep_ == "attr"

            return noun.head != head or head_is_attr
        return True

    @staticmethod
    def get_noun_after_prep(tokens: List[Token]):
        prep_rights = [prep for prep in tokens if is_preposition(prep)]

        if len(prep_rights) > 0:
            head = prep_rights[0]
            noun_rights = TokenHandler.get_nouns(list(head.rights))

            if len(noun_rights) > 0:
                # E.g.: "Give me the currency of China."
                # E.g.: "Who were the parents of Queen Victoria?"
                # E.g.: "Which soccer players were born on Malta?"
                # E.g.: "Which museum in New York has the most visitors?"
                return noun_rights[0]

        return None

    @staticmethod
    def get_nouns(tokens: List[Token], dep_list: List[str] = None):
        noun_list = []

        for token in tokens:
            if is_noun(token):
                if dep_list is not None:
                    if token.dep_ in dep_list:
                        noun_list.append(token)
                else:
                    noun_list.append(token)
            elif is_preposition(token):
                if token.i > 0:
                    # E.g.: token.i == 0 => In which country is Mecca located?
                    next_word = get_next_word(token)
                    if is_noun(next_word):
                        noun_list.append(next_word)

                    # E.g.: "Who is the author of the interpretation of dreams?"
                    if next_word.dep_ == "det":
                        next_word = get_next_word(next_word)
                    if is_noun(next_word):
                        noun_list.append(next_word)

        # E.g.: "What is the birth name of Adele?"
        return list(set(noun_list))

    @staticmethod
    def get_adjectives(tokens: List[Token], exceptions: List[str] = None):
        adjectives = []

        for token in tokens:
            if is_adj(token):
                if exceptions is not None:
                    if token.lower_ not in exceptions:
                        # E.g.: "Who is the current federal minister of finance in Germany?"
                        adjectives.append(token)
                else:
                    adjectives.append(token)

        return adjectives
