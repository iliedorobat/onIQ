from typing import List

from spacy.tokens import Token

from ro.webdata.oniq.common.nlp.utils import WordnetUtils
from ro.webdata.oniq.common.nlp.word_utils import is_preposition, is_noun
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

        return noun_list
