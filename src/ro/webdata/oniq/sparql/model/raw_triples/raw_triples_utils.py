from ro.webdata.oniq.common.nlp.word_utils import is_adj, is_wh_word
from ro.webdata.oniq.sparql.common.TokenHandler import TokenHandler
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, QUESTION_TYPES
from ro.webdata.oniq.sparql.model.raw_triples.RawTripleGenerator import RawTripleGenerator, STATEMENT_TYPE


def prepare_base_raw_triples(nl_question: NLQuestion):
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

        generator.append_noun_triple(subject, p, obj)

        # E.g.: "Which museum in New York has the most visitors?"
        generator.append_triple(subject, head, STATEMENT_TYPE.NOUN)

        # E.g.: "How many companies were founded by the founder of Facebook?" => founder of Facebook
        generator.append_triple(obj, head, STATEMENT_TYPE.NOUN)

        generator.append_triple(head, head, STATEMENT_TYPE.PASS_POSS)
    else:
        if len(noun_rights) > 0:
            adj_lefts = [token for token in lefts if is_adj(token)]
            if len(adj_lefts) > 0:
                # E.g.: "How high is the Yokohama Marine Tower?"
                generator.append_triple(noun_rights[0], adj_lefts[0], STATEMENT_TYPE.ADJECTIVE)

            statement = RawTripleGenerator.passive_possessive_handler(question, noun_rights[0])
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
                generator.append_triple(head, head, STATEMENT_TYPE.NOUN)

                if len(noun_lefts) > 0:
                    if len(noun_rights) > 0:
                        # E.g.: "Is Barack Obama a democrat?"
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

                adj_lefts = [token for token in list(head.lefts) if is_adj(token)]
                if len(adj_lefts) > 0:
                    # E.g.: "Give me all Swedish holidays."
                    # E.g.: "Who is the youngest Pulitzer Prize winner?"
                    # E.g.: "Who was the doctoral advisor of Albert Einstein" => "doctoral".dep_ == "amod"
                    generator.append_triple(head, adj_lefts[0], STATEMENT_TYPE.ADJECTIVE)

    return generator.raw_triples
