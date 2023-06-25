from typing import List

from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.nlp_utils import token_to_span
from ro.webdata.oniq.common.nlp.utils import WordnetUtils
from ro.webdata.oniq.common.nlp.word_utils import is_preposition, is_noun, is_adj, is_wh_word, is_aux
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.sparql.model.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


def prepare_raw_triples(sentence: Span):
    raw_triples = []

    head = sentence.root
    lefts = [token for token in list(head.lefts) if not is_wh_word(token)]
    rights = [token for token in list(head.rights) if not is_wh_word(token)]

    noun_lefts = _get_nouns(lefts)
    noun_rights = _get_nouns(rights)

    if len(noun_lefts) > 0:
        subject = noun_lefts[0]
        p = token_to_span(head)
        obj = None

        if len(noun_rights) > 0:
            # E.g.: "Did Arnold Schwarzenegger attend a university?"
            obj = noun_rights[0]
        else:
            # E.g.: "Which soccer players were born on Malta?"
            obj = _get_noun_after_prep(rights)
            if obj is None:
                # E.g.: "Which volcanos in Japan erupted since 2000?"
                # E.g.: "When did the Ming dynasty dissolve?"
                obj = p[0].text

        statement = RawTriple(
            s=NounEntity(subject),
            p=p,
            o=NounEntity(obj),
            question=sentence
        )
        raw_triples.append(statement)

        # E.g.: "Which museum in New York has the most visitors?"
        statement = _RawTripleHandler.prep_after_noun(sentence, subject)
        if statement is not None:
            raw_triples.append(statement)

        # E.g.: "How many companies were founded by the founder of Facebook?" => founder of Facebook
        statement = _RawTripleHandler.prep_after_noun(sentence, obj)
        if statement is not None:
            raw_triples.append(statement)

        statement = _RawTripleHandler.passive_possessive(sentence, head)
        if statement is not None:
            raw_triples.append(statement)
    else:
        if len(noun_rights) > 0:
            adj_lefts = [token for token in lefts if is_adj(token)]

            if len(adj_lefts) > 0:
                # E.g.: "How high is the Yokohama Marine Tower?"
                adjective = adj_lefts[0]

                if _adj_not_found(adjective, head):
                    statement = RawTriple(
                        s=NounEntity(noun_rights[0]),
                        p=token_to_span(adjective),
                        o=AdjectiveEntity(adjective),
                        question=sentence
                    )
                    raw_triples.append(statement)

            statement = _RawTripleHandler.passive_possessive(sentence, noun_rights[0])
            if statement is not None:
                raw_triples.append(statement)
            else:
                # E.g.: "Who is the youngest Pulitzer Prize winner?"
                head = noun_rights[0]
                noun_lefts = _get_nouns(list(head.lefts))
                noun_rights = _get_nouns(list(head.rights))

                # E.g.: "Give me the currency of China."
                # E.g.: "Who were the parents of Queen Victoria?"
                # E.g.: "What is the highest mountain in Romania?"
                statement = _RawTripleHandler.prep_after_noun(sentence, head)
                if statement is not None:
                    raw_triples.append(statement)

                if len(noun_lefts) > 0:
                    if len(noun_rights) > 0:
                        # E.g.: "Is Barack Obama a democrat?"
                        statement = RawTriple(
                            s=NounEntity(head),
                            p="?prop",
                            o=NounEntity(noun_rights[0]),
                            question=sentence
                        )
                        raw_triples.append(statement)
                    else:
                        if _noun_not_found(noun_lefts[0], head):
                            statement = RawTriple(
                                s=head.lemma_,
                                p="?prop",
                                o=NounEntity(noun_lefts[0]),
                                question=sentence
                            )
                            raw_triples.append(statement)
                        else:
                            # TODO: E.g.: "Give me all ESA astronauts."
                            pass

                # E.g.: "Give me all Swedish holidays."
                # E.g.: "Who is the youngest Pulitzer Prize winner?"
                # E.g.: "Who was the doctoral advisor of Albert Einstein" => "doctoral".dep_ == "amod"
                adj_lefts = [token for token in list(head.lefts) if is_adj(token)]
                if len(adj_lefts) > 0:
                    adjective = adj_lefts[0]
                    country = WordnetUtils.find_country_by_nationality(adjective.text)

                    if _adj_not_found(adjective, head):
                        statement = RawTriple(
                            s=head.lemma_,
                            p="country" if country is not None else token_to_span(adjective),
                            o=country if country is not None else AdjectiveEntity(adjective),
                            question=sentence
                        )
                        raw_triples.append(statement)

    return raw_triples


class _RawTripleHandler:
    @staticmethod
    def prep_after_noun(sentence: Span, noun: Token):
        noun_entity = NounEntity(noun)

        if noun_entity.is_text():
            # E.g.: "When did the Ming dynasty dissolve?"
            return None

        rights = list(noun_entity.token.rights)
        prep = _RawTripleHandler._get_prep(rights)

        if prep is not None:
            noun = _get_noun_after_prep(rights)

            if prep.lower_ == "in":
                # E.g.: "What is the highest mountain in Romania?"
                return RawTriple(
                    s=NounEntity(noun_entity.token),
                    p=token_to_span(prep),
                    o=NounEntity(noun),
                    question=sentence
                )
            elif prep.lower_ == "of":
                # E.g.: "Give me the currency of China."
                return RawTriple(
                    s=NounEntity(noun),
                    p=noun_entity.to_span(),
                    o=NounEntity(noun_entity.token),
                    question=sentence
                )

        return None

    @staticmethod
    def passive_possessive(sentence: Span, token: Token):
        lefts = [token for token in list(token.lefts) if not is_wh_word(token)]
        rights = [token for token in list(token.rights) if not is_wh_word(token)]

        if len(rights) > 0 and is_aux(rights[0]):
            # E.g.: "Who is the person whose successor was Le Hong Phong?"  # possessive
            # E.g.: "Where was the person born whose successor was Le Hong Phong?"  # passive
            token = rights[0]
            noun_lefts = _get_nouns(list(token.lefts))
            noun_rights = _get_nouns(list(token.rights))

            if len(noun_lefts) > 0 and len(noun_rights) > 0:
                return RawTriple(
                    s=NounEntity(noun_lefts[0]),
                    p=token_to_span(noun_lefts[0]),
                    o=NounEntity(noun_rights[0]),
                    question=sentence
                )

        return None

    @staticmethod
    def _get_prep(tokens: List[Token]):
        prep_rights = [prep for prep in tokens if is_preposition(prep)]

        if len(prep_rights) > 0:
            return prep_rights[0]

        return None


def _get_noun_after_prep(tokens: List[Token]):
    prep_rights = [prep for prep in tokens if is_preposition(prep)]

    if len(prep_rights) > 0:
        head = prep_rights[0]
        noun_rights = _get_nouns(list(head.rights))

        if len(noun_rights) > 0:
            # E.g.: "Give me the currency of China."
            # E.g.: "Who were the parents of Queen Victoria?"
            # E.g.: "Which soccer players were born on Malta?"
            # E.g.: "Which museum in New York has the most visitors?"
            return noun_rights[0]

    return None


def _get_nouns(tokens: List[Token], exception: Token = None):
    noun_list = []

    for token in tokens:
        if is_noun(token):
            if exception is None:
                noun_list.append(token)
            elif exception.dep_ == "attr":
                # E.g.: "Who is the youngest Pulitzer Prize winner?"
                noun_list.append(token)
            else:
                exception_text = NounEntity(exception).text
                if token.text in exception_text:
                    # E.g.: "Is Barack Obama a democrat?"
                    continue

    return noun_list


def _adj_not_found(adjective: Token, head: Token):
    adjective_cond = True
    country_cond = True

    if is_noun(head):
        country = WordnetUtils.find_country_by_nationality(adjective.text)

        if country is None:
            # E.g.: "What is the net income of Apple?"
            # E.g.: "How high is the Yokohama Marine Tower?"
            adjective_cond = adjective.lower_ not in NounEntity(head).to_span().text.lower()
        else:
            # E.g.: "Give me all Swedish holidays." => country is not None
            country_cond = country.lower() not in NounEntity(head).to_span().text.lower()

    return country_cond and adjective_cond


def _noun_not_found(noun: Token, head: Token):
    if is_noun(noun):
        # E.g.: "How high is the Yokohama Marine Tower?" => noun.text in NounEntity(head).text
        return noun.lower_ not in NounEntity(head).to_span().text.lower()
    return True
