from ro.webdata.oniq.common.nlp.word_utils import is_adj, is_wh_word, is_aux, is_noun, get_prev_word, is_preposition
from ro.webdata.oniq.sparql.NLQuestion import NLQuestion, QUESTION_TYPES
from ro.webdata.oniq.sparql.NounEntity import NounEntity
from ro.webdata.oniq.sparql.common.TokenHandler import TokenHandler
from ro.webdata.oniq.sparql.triples.raw_triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.triples.raw_triples.RawTripleGenerator import STATEMENT_TYPE, RawTripleGenerator
from ro.webdata.oniq.sparql.triples.raw_triples.generator.RawTripleHandler import RawTripleHandler


class RawTriples:
    def __init__(self, nl_question: NLQuestion):
        self.values = init_raw_triples(nl_question)


def init_raw_triples(nl_question: NLQuestion):
    generator = RawTripleGenerator(nl_question)
    question = nl_question.question
    head = question.root

    lefts = [token for token in list(head.lefts) if not is_wh_word(token)]
    rights = [token for token in list(head.rights) if not is_wh_word(token)]

    noun_lefts = TokenHandler.get_nouns(lefts)
    noun_rights = TokenHandler.get_nouns(rights)

    if len(noun_lefts) > 0:
        subject = noun_lefts[0]
        p = head
        obj = None

        if nl_question.question_type == QUESTION_TYPES.S_PREP:
            # E.g.: "In which country is Mecca located?"
            rights_prep = list(question[0].rights)
            noun_rights_prep = TokenHandler.get_nouns(rights_prep)

            if len(noun_rights_prep) > 0:
                p = noun_rights_prep[0]

        if len(noun_rights) > 0:
            # E.g.: "Did Arnold Schwarzenegger attend a university?"
            obj = noun_rights[0]
        else:
            # E.g.: "Which soccer players were born on Malta?"
            obj = TokenHandler.get_noun_after_prep(rights)
            if obj is None:
                # E.g.: "Which volcanos in Japan erupted since 2000?"
                # E.g.: "When did the Ming dynasty dissolve?"
                obj = p

        if obj.lemma_ == "have":
            aux_lefts = [token for token in list(obj.lefts) if is_aux(token)]
            if len(aux_lefts) > 0:
                nsubj_lefts = TokenHandler.get_nouns(noun_lefts, ["nsubj", "nsubjpass"])
                dobj_lefts = [token for token in noun_lefts if token.dep_ == "dobj"]
                if len(nsubj_lefts) > 0 and len(dobj_lefts) > 0:
                    # E.g.: "How many children does Eddie Murphy have?"
                    subject = nsubj_lefts[0]
                    p = dobj_lefts[0]
                    obj = dobj_lefts[0]

                n_lefts = [token for token in list(aux_lefts[0].lefts) if is_noun(token)]
                if len(n_lefts) > 0:
                    # E.g.: "How many children did Benjamin Franklin have?"
                    p = n_lefts[0]
                    obj = n_lefts[0]
        elif p.lemma_ == "have" and NounEntity(obj).is_res():
            # E.g.: "How many awards has Bertrand Russell?"
            old_subject = subject
            subject = obj
            p = old_subject
            obj = old_subject

        generator.append_noun_triple(subject, p, obj)

        # E.g.: "Which museum in New York has the most visitors?"
        generator.append_triple(subject, None, STATEMENT_TYPE.NOUN)

        # E.g.: "How many companies were founded by the founder of Facebook?" => founder of Facebook
        generator.append_triple(obj, None, STATEMENT_TYPE.NOUN)

        generator.append_triple(head, None, STATEMENT_TYPE.PASS_POSS)
    else:
        if len(noun_rights) > 0:
            # TODO: replace with RawTripleGenerator.append_triple
            statement = RawTripleHandler.passive_possessive_handler(question, noun_rights[0])
            if statement is not None:
                generator.raw_triples.append(statement)
            else:
                # E.g.: "Who is the youngest Pulitzer Prize winner?"
                head = noun_rights[0]
                noun_lefts = TokenHandler.get_nouns(list(head.lefts))
                noun_rights = TokenHandler.get_nouns(list(head.rights))

                # E.g.: "Give me the currency of China."
                # E.g.: "Who were the parents of Queen Victoria?"
                # E.g.: "What is the highest mountain in Romania?"
                generator.append_triple(head, None, STATEMENT_TYPE.NOUN)

                if len(noun_lefts) > 0:
                    if len(noun_rights) > 0:
                        # E.g.: "Is Barack Obama a democrat?"
                        prev_word = get_prev_word(noun_rights[0])
                        if not is_preposition(prev_word):
                            # E.g.: "What is the birth name of Adele?" => is_preposition(prev_word)
                            generator.append_noun_triple(head, "?property", noun_rights[0])
                    else:
                        if TokenHandler.noun_not_found(noun_lefts[0], head):
                            # E.g.: "Who is the youngest Pulitzer Prize winner?"
                            generator.append_noun_triple(head, head, noun_lefts[0])
                        elif head.dep_ == "dobj":
                            # E.g.: "Give me all ESA astronauts."
                            generator.append_noun_triple(head.text, "?property", noun_lefts[0])
                        else:
                            # E.g.: "How high is the Yokohama Marine Tower?"
                            # do nothing
                            pass
                # else:
                #     if len(noun_rights) > 0:
                #         # E.g.: "What is the smallest city by area in Germany?"
                #         generator.append_triple(noun_rights[0], None, STATEMENT_TYPE.NOUN)

                adj_lefts = TokenHandler.get_adjectives(list(head.lefts), ["current"])
                if len(adj_lefts) > 0:
                    # E.g.: "Give me all Swedish holidays."
                    # E.g.: "Who is the youngest Pulitzer Prize winner?"
                    # E.g.: "Who was the doctoral advisor of Albert Einstein" => "doctoral".dep_ == "amod"

                    order_by_adj = [
                        triple for triple in generator.raw_triples
                        if triple.order_by is not None
                           and triple.order_by.order_by_token == adj_lefts[0]
                    ]
                    if len(order_by_adj) == 0:
                        # E.g.: "What is the smallest city by area in Germany?" => len(order_by_adj) > 0
                        generator.append_triple(head, adj_lefts[0], STATEMENT_TYPE.ADJECTIVE)

            if len(generator.raw_triples) == 0:
                # E.g.: "How large is the area of UK?"              => len(generator.raw_triples) > 0
                # E.g.: "How high is the Yokohama Marine Tower?"    => len(generator.raw_triples) == 0
                adj_lefts = TokenHandler.get_adjectives(lefts)
                if len(adj_lefts) > 0:
                    # E.g.: "How high is the Yokohama Marine Tower?"
                    noun_rights = TokenHandler.get_nouns(rights)
                    generator.append_triple(noun_rights[0], adj_lefts[0], STATEMENT_TYPE.ADJECTIVE)

    if len(generator.raw_triples) == 0:
        if nl_question.question_type == QUESTION_TYPES.WHO:
            # E.g.: "Who is Dan Jurafsky?"
            subject = "VALUES"
            p = head
            obj = head

            statement = RawTriple(
                s=subject,
                p=p,
                o=NounEntity(obj),
                question=question
            )
            generator.raw_triples.append(statement)

    return generator.raw_triples
