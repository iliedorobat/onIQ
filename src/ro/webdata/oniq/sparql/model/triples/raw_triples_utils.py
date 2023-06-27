from spacy.tokens import Span

from ro.webdata.oniq.common.nlp.nlp_utils import token_to_span
from ro.webdata.oniq.common.nlp.utils import WordnetUtils
from ro.webdata.oniq.common.nlp.word_utils import is_adj, is_wh_word
from ro.webdata.oniq.sparql.model.AdjectiveEntity import AdjectiveEntity
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.model.triples.RawTripleGenerator import RawTripleGenerator
from ro.webdata.oniq.sparql.model.triples.TokenHandler import TokenHandler


# TODO: rename to prepare_base_raw_triples
def prepare_raw_triples(sentence: Span):
    raw_triples = []

    head = sentence.root
    lefts = [token for token in list(head.lefts) if not is_wh_word(token)]
    rights = [token for token in list(head.rights) if not is_wh_word(token)]

    noun_lefts = TokenHandler.get_nouns(lefts)
    noun_rights = TokenHandler.get_nouns(rights)

    if len(noun_lefts) > 0:
        subject = noun_lefts[0]
        p = token_to_span(head)
        obj = None

        if len(noun_rights) > 0:
            # E.g.: "Did Arnold Schwarzenegger attend a university?"
            obj = noun_rights[0]
        else:
            # E.g.: "Which soccer players were born on Malta?"
            obj = TokenHandler.get_noun_after_prep(rights)
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
        statement = RawTripleGenerator.prep_after_noun_handler(sentence, subject)
        if statement is not None:
            raw_triples.append(statement)

        # E.g.: "How many companies were founded by the founder of Facebook?" => founder of Facebook
        statement = RawTripleGenerator.prep_after_noun_handler(sentence, obj)
        if statement is not None:
            raw_triples.append(statement)

        statement = RawTripleGenerator.passive_possessive_handler(sentence, head)
        if statement is not None:
            raw_triples.append(statement)
    else:
        if len(noun_rights) > 0:
            adj_lefts = [token for token in lefts if is_adj(token)]

            if len(adj_lefts) > 0:
                # E.g.: "How high is the Yokohama Marine Tower?"
                adjective = adj_lefts[0]

                if TokenHandler.adj_not_found(adjective, head):
                    statement = RawTriple(
                        s=NounEntity(noun_rights[0]),
                        p=token_to_span(adjective),
                        o=AdjectiveEntity(adjective),
                        question=sentence
                    )
                    raw_triples.append(statement)

            statement = RawTripleGenerator.passive_possessive_handler(sentence, noun_rights[0])
            if statement is not None:
                raw_triples.append(statement)
            else:
                # E.g.: "Who is the youngest Pulitzer Prize winner?"
                head = noun_rights[0]
                noun_lefts = TokenHandler.get_nouns(list(head.lefts))
                noun_rights = TokenHandler.get_nouns(list(head.rights))

                # E.g.: "Give me the currency of China."
                # E.g.: "Who were the parents of Queen Victoria?"
                # E.g.: "What is the highest mountain in Romania?"
                statement = RawTripleGenerator.prep_after_noun_handler(sentence, head)
                if statement is not None:
                    raw_triples.append(statement)

                if len(noun_lefts) > 0:
                    if len(noun_rights) > 0:
                        # E.g.: "Is Barack Obama a democrat?"
                        statement = RawTriple(
                            s=NounEntity(head),
                            p="?property",
                            o=NounEntity(noun_rights[0]),
                            question=sentence
                        )
                        raw_triples.append(statement)
                    else:
                        # E.g.: "Who is the youngest Pulitzer Prize winner?"
                        if TokenHandler.noun_not_found(noun_lefts[0], head):
                            statement = RawTriple(
                                s=head,
                                p=token_to_span(head),
                                o=NounEntity(noun_lefts[0]),
                                question=sentence
                            )
                            raw_triples.append(statement)
                        # else:
                        #     # TODO: E.g.: "Give me all ESA astronauts."
                        #     pass

                # E.g.: "Give me all Swedish holidays."
                # E.g.: "Who is the youngest Pulitzer Prize winner?"
                # E.g.: "Who was the doctoral advisor of Albert Einstein" => "doctoral".dep_ == "amod"
                adj_lefts = [token for token in list(head.lefts) if is_adj(token)]
                if len(adj_lefts) > 0:
                    adjective = adj_lefts[0]
                    country = WordnetUtils.find_country_by_nationality(adjective.text)

                    if TokenHandler.adj_not_found(adjective, head):
                        statement = RawTriple(
                            s=head,
                            p="country" if country is not None else token_to_span(adjective),
                            o=NounEntity(adjective) if country is not None else AdjectiveEntity(adjective),
                            question=sentence
                        )
                        raw_triples.append(statement)

    return raw_triples
