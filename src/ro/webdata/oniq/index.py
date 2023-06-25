from typing import List

from spacy import displacy
from spacy.tokens.token import Token

from ro.webdata.oniq.common.nlp.word_utils import is_noun, is_preposition, is_wh_word, is_adj
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.endpoint.dbpedia.setup import DBpediaSetup
from ro.webdata.oniq.spacy_model import nlp_model
from ro.webdata.oniq.validation.pre_validation_pairs.pairs import PAIRS
from ro.webdata.oniq.validation.pre_validation_pairs.pairs_qald_5_test import PAIRS_QALD
from ro.webdata.oniq.validation.validation_pairs.pairs_qald_5_test import PAIRS_QALD as V_PAIRS_QALD
from ro.webdata.oniq.validation.validation import question_test, questions_test

ENDPOINT = "http://localhost:7200/repositories/TESTING_BCU_CLUJ"
ENDPOINT = "http://localhost:7200/repositories/eCHO"


# QUERY = "Where is Fort Knox?"  # FIXME
# QUERY = "At what distance does the earth curve?"  # FIXME:
# QUERY = "Did Raymond Picard take birth in Paris?"  # TODO:
# TODO: identificarea types-ului: "which artists were born..." => ?artists born ?thing   ?artists rdf:tpe dbo:Artists
QUERY = "Who won the Pulitzer Prize?"  # FIXME:
QUERY = "Give me all the female astronauts."  # FIXME: derived from "Give me all ESA astronauts."


QUERY = "Is Lake Baikal bigger than the Great Bear Lake?"
QUERY = "Desserts from which country contain fish?"  # TODO:
# QUERY = "Give me all Swiss non-profit organizations."
# QUERY = "Who killed John Lennon?"  # ??
# QUERY = "Who is starring in Spanish movies produced by Benicio del Toro?"
# QUERY = "What is the height difference between Mount Everest and K2?"
# QUERY = "What does the abbreviation FIFA stand for?"
# QUERY = "How high is the Yokohama Marine Tower?"  # ??
# QUERY = "How many scientists graduated from an Ivy League university?"  # ??
# QUERY = "How many companies were founded by the founder of Facebook?"
# QUERY = "How many companies were founded in the same year as Google?"
# QUERY = "Which animals are critically endangered?"
# QUERY = "Which programming languages were influenced by Perl?"
# QUERY = "Which artists were born on the same date as Rachel Stevens?"
# QUERY = "Which types of grapes grow in Oregon?"
# QUERY = "Which movies starring Brad Pitt were directed by Guy Ritchie?"
# QUERY = "Which subsidiary of Lufthansa serves both Dortmund and Berlin Tegel?"
QUERY = "Which musician wrote the most books?"
# QUERY = "Which Greek parties are pro-European?"
# QUERY = "Which volcanos in Japan erupted since 2000?"

# QUERY = "Where is adam mickiewicz monument?"  # FIXME:
# QUERY = "Which museum hosts more than 10 pictures and exposed one sword?"  # TODO:


QUERY = "Who is the youngest Pulitzer Prize winner?"
# QUERY = "Who is the tallest basketball player?"
QUERY = "What is the federated state located in the Weimar Republic?"
QUERY = "Did Steve Sampson manage a club of Santa Clara university"
QUERY = "Who was nominated for an Academy Award for  Best Sound Mixing in Gladiator?"
QUERY = "In what year did Tim Hunt give a Croonian Lecture?"
QUERY = "When was Bibi Andersson married to Per Ahlmark?"
QUERY = "Where does the holder of the position of Lech Kaczynski live?"
QUERY = "Who wrote the singles on the Main Course?"
QUERY = "Who is the father and mother of Janet Jackson?"  # TODO: and

# https://github.com/ag-sc/QALD/blob/master/8/data/qald-8-test-multilingual.json
QUERY = "Where is the origin of Carolina reaper?"  # ID 17
QUERY = "How much is the population of Mexico City ?"  # ID 18
QUERY = "What is the nick name of Baghdad?"  # ID 19
QUERY = "How much is the population of Iraq?"  # ID 22 (total population)
#
# sparql_query = SPARQLBuilder(ENDPOINT, QUERY)

# QUERY = "Who is the person whose successor was Le Hong Phong?"  # poss
# QUERY = "Where was the designer of REP Parasol born?"
QUERY = "Which volcanos in Japan erupted since 2000?"



QUERY = "Did Arnold Schwarzenegger attend a university?"  # OK
QUERY = "Is Barack Obama a democrat?"  # OK
QUERY = "In which country is Mecca located?"  # OK
QUERY = "Give me all ESA astronauts."  # OK
QUERY = "Give me all Swedish holidays."  # OK
QUERY = "Give me the currency of China."  # OK
QUERY = "When did the Ming dynasty dissolve?"  # OK
QUERY = "Who is the manager of Real Madrid?"  # OK
QUERY = "Who were the parents of Queen Victoria?"  # OK
QUERY = "Who is the youngest Pulitzer Prize winner?"  # OK
# QUERY = "Who is the oldest child of Meryl Streep?"  ### OK => FIXME!!! => FIXME: transitivity of nodes
QUERY = "Who is the tallest basketball player?"  # OK
QUERY = "What is the net income of Apple?"  # OK
QUERY = "What is the highest mountain in Italy?"  # OK
QUERY = "How high is the Yokohama Marine Tower?"  # OK
# QUERY = "How many ethnic groups live in Slovenia?"  # FIXME: transitivity of nodes
QUERY = "Which soccer players were born on Malta?"  # OK
QUERY = "Which museum in New York has the most visitors?"  # OK => FIXME: => New_York_City insted of New_York_(state) and dbo:numberOfVisitors instead of dbp:visitors
# QUERY = "Who was the doctoral advisor of Albert Einstein"



# QUERY = "Which Indian company has the most employees?"
# QUERY = "What is the population and area of the most populated state?"
# QUERY = "Which museum in New York has the fewest visitors?"
# QUERY = "Which musician wrote the most books?"
QUERY = "Desserts from which country contain fish?"  # FIXME:
QUERY = "Which country has fish in its deserts?"  # FIXME:

QUERY = "How many ethnic groups live in Slovenia"
QUERY = "What is the highest mountain in Italy?"
# QUERY = "What mountains are located in Italy?"

QUERY = "How many ethnic groups live in Slovenia?"
QUERY = "Which animals are critically endangered?"
QUERY = "Which musician wrote the most books?"
# QUERY = "Which is the most important building?"

QUERY = "How many companies were founded in the same year as Google?"
QUERY = "Which Indian company has the most employees?"
# QUERY = "Who is the Prime Minister of India?"
QUERY = "Who was married to an actor that played in Philadelphia?"
# QUERY = "where was the person who won the oscar born?"
# QUERY = "Which soccer players were born on Malta?"
QUERY = "Give me all Argentine films."  # FIXME: films => movie
QUERY = "Who was the father of Queen Elizabeth II?"

# DBpediaQueryService.run_main_classes_query()

QUERY = "Which soccer players were born on Malta?"
QUERY = "Who is the person whose successor was Le Hong Phong?"
QUERY = "Whose successor is Le Hong Phong?"
# QUERY = "Who is the leader of the town where the Myntdu river originates?"
# QUERY = "where was the person who won the oscar born?"
# QUERY = "Which soccer players were born on Malta?"
# QUERY = "How high is the Yokohama Marine Tower?"
# QUERY = "Did Arnold Schwarzenegger attend a university?"

# QUERY = "How many people live in Romania?"
# QUERY = "Who was married to an actor that played in Philadelphia?"


# QUERY = "Did Arnold Schwarzenegger attend a university?"  # OK ===
QUERY = "Is Barack Obama a democrat?"  # OK
# QUERY = "In which country is Mecca located?"  # OK ===
# QUERY = "Give me all ESA astronauts."  # OK ===
# QUERY = "Give me all Swedish holidays."  # OK ===
# QUERY = "Give me the currency of China."  # OK ===
# QUERY = "When did the Ming dynasty dissolve?"  # OK ===
# QUERY = "Who is the manager of Real Madrid?"  # OK ===
# QUERY = "Who were the parents of Queen Victoria?"  # OK ===
# QUERY = "Who is the youngest Pulitzer Prize winner?"  # OK ===
# QUERY = "Who is the oldest child of Meryl Streep?"  ### OK
# QUERY = "Who is the tallest basketball player?"  # OK ===
# QUERY = "What is the net income of Apple?"  # OK
# QUERY = "What is the highest mountain in Italy?"  # OK ===
# QUERY = "How high is the Yokohama Marine Tower?"  # OK ===
# QUERY = "How many ethnic groups live in Slovenia?"  # OK === it is not ok
# QUERY = "Which soccer players were born on Malta?"  # OK ===
# QUERY = "Which museum in New York has the most visitors?"  # OK ===

# TODO: check
QUERY = "Give me all Swiss non-profit organizations."
QUERY = "How many companies were founded by the founder of Facebook?"

import spacy
nlp = spacy.load('en_core_web_md')
doc = nlp(QUERY)


# def _get_noun_after_prep(tokens: List[Token]):
#     prep_rights = [prep for prep in tokens if is_preposition(prep)]
#
#     if len(prep_rights) > 0:
#         rights = list(prep_rights[0].rights)
#         noun_rights = [noun for noun in rights if is_noun(noun)]
#
#         if len(noun_rights) > 0:
#             # E.g.: "Which soccer players were born on Malta?"
#             return noun_rights[0]


for sent in doc.sents:
    print(sent)

    root = sent.root
    lefts = [token for token in list(root.lefts) if not is_wh_word(token)]
    rights = [token for token in list(root.rights) if not is_wh_word(token)]

    noun_lefts = [noun for noun in lefts if is_noun(noun)]
    noun_rights = [noun for noun in rights if is_noun(noun)]

    if len(noun_lefts) > 0:
        s = noun_lefts[0]
        p = root
        o = None

        if len(noun_rights) > 0:
            o = noun_rights[0]
        else:
            prep_rights = [prep for prep in rights if is_preposition(prep)]

            if len(prep_rights) > 0:
                rights = list(prep_rights[0].rights)
                noun_rights = [noun for noun in rights if is_noun(noun)]

                if len(noun_rights) > 0:
                    # E.g.: "Which soccer players were born on Malta?"
                    o = noun_rights[0]

                    # TODO: "How many companies were founded by the founder of Facebook?" => founder of Facebook

        print(f"{s}   {p}   {o}")

        root = noun_lefts[0]
        lefts = list(root.lefts)
        rights = list(root.rights)

        # prep_lefts = [prep for prep in lefts if is_preposition(prep)]
        prep_rights = [prep for prep in rights if is_preposition(prep)]

        if len(prep_rights) > 0:
            root = prep_rights[0]
            # lefts = list(root.lefts)
            # noun_lefts = [noun for noun in lefts if is_noun(noun)]

            rights = list(root.rights)
            noun_rights = [noun for noun in rights if is_noun(noun)]

            if len(noun_rights) > 0:
                # E.g.: "Which museum in New York has the most visitors?"
                o = noun_rights[0]
                p = root
                print(f"{s}   {p}   {o}")
    else:
        if len(noun_rights) > 0:
            adj_lefts = [token for token in lefts if is_adj(token)]
            if len(adj_lefts) > 0:
                # E.g.: "How high is the Yokohama Marine Tower?"
                s = noun_rights[0]
                o = adj_lefts[0]
                p = o

                print(f"{s}   {p}   {o}")
            else:
                prep_rights = [prep for prep in list(noun_rights[0].rights) if is_preposition(prep)]

                if len(prep_rights) > 0:
                    o = noun_rights[0]
                    p = o

                    rights = list(prep_rights[0].rights)
                    noun_rights = [noun for noun in rights if is_noun(noun)]

                    if len(noun_rights) > 0:
                        # E.g.: "Give me the currency of China."
                        s = noun_rights[0]

                        print(f"{s}   {p}   {o}")

                # E.g.: "Give me all Swedish holidays."
                adj_lefts = [token for token in list(noun_rights[0].lefts) if is_adj(token)]
                if len(adj_lefts) > 0:
                    s = noun_rights[0]
                    o = adj_lefts[0]
                    p = o

                    print(f"{s}   {p}   {o}")

                # E.g.: "Give me all ESA astronauts."
                noun_lefts = [token for token in list(noun_rights[0].lefts) if is_noun(token)]
                if len(noun_lefts) > 0:
                    # TODO: check "Who were the parents of Queen Victoria?"
                    # TODO: check "Is Barack Obama a democrat?"
                    s = noun_rights[0]
                    o = noun_lefts[0]
                    p = o

                    print(f"{s}   {p}   {o}")

        elif len(rights) > 0:
            s = rights[0]
            o = rights[0]
            p = o

            rights = list(o.rights)
            lefts = list(o.lefts)

            adj_lefts = [token for token in lefts if is_adj(token)]
            noun_lefts = [token for token in lefts if is_noun(token)]
            prep_rights = [token for token in rights if is_preposition(token)]

            if len(prep_rights) > 0:
                prep = prep_rights[0]
                rights = list(prep.rights)
                noun_rights = [noun for noun in rights if is_noun(noun)]

                if len(noun_rights) > 0:
                    # E.g.: "Who were the parents of Queen Victoria?"
                    if prep.lower_ == "of":
                        s = noun_rights[0]
                    elif prep.lower_ == "in":
                        # E.g.: "What is the highest mountain in Romania?"
                        s = o
                        o = noun_rights[0]
                        p = o
                    print(f"{s}   {p}   {o}")

            if len(noun_lefts) > 0:
                # E.g.: "Who is the youngest Pulitzer Prize winner?"
                o = noun_lefts[0]
                print(f"{s}   {p}   {o}")

            if len(adj_lefts) > 0:
                # E.g.: "What is the highest mountain in Romania?"
                adj = adj_lefts[0]
                p = adj
                o = adj
                print(f"{s}   {p}   {o}")

    pass

# import spacy
# import spacy_dbpedia_spotlight
#
#
# nlp = spacy.load('en_core_web_md')
# nlp.add_pipe('dbpedia_spotlight', config={'confidence': 0.75})
#
# doc = nlp(QUERY)
# for ent in doc.ents:
#     # print(ent.text)
#     raw_result = ent._.dbpedia_raw_result
#     print(ent.text, ent.kb_id_, raw_result['@similarityScore'] if raw_result is not None else None)


print_summary = True
print_deps = True
raw_test = False
#
question_test(PAIRS_QALD, QUERY, True, print_summary, print_deps)
# question_test(V_PAIRS_QALD, QUERY, False, print_summary, print_deps)

# print("Validating Raw SPARQL Queries...\n")
# questions_test(PAIRS_QALD, True, print_summary, print_deps)
# questions_test(PAIRS, True, print_summary, print_deps)

# print("Validating Final SPARQL Queries...\n")
# questions_test(V_PAIRS_QALD, False, True, True)

# nlp_query = nlp_model(QUERY)
# displacy.serve(nlp_query, style="dep")

# TODO:
# if GLOBAL_ENV.TEST_MODE == TEST_MODES.DEFAULT:
#     sparql_query = SPARQLBuilder(ENDPOINT, QUERY, print_deps)
# elif GLOBAL_ENV.TEST_MODE == TEST_MODES.LOCAL_TEST:
#     question_test(V_PAIRS_QALD, QUERY, raw_test, print_summary, print_deps)
#     # question_test(PAIRS, QUERY, raw_test, print_summary, print_deps)
#
#     # questions_test(PAIRS_QALD, raw_test, print_summary, print_deps)
#     # questions_test(PAIRS, raw_test, print_summary, print_deps)
# else:
#     questions_test(PAIRS_QALD, raw_test, print_summary, print_deps)
#     questions_test(PAIRS, raw_test, print_summary, print_deps)
#



# TODO: test: TeBaQA:
#  webservice: https://tebaqa.demos.dice-research.org/qa-simple
#  github repo: https://github.com/dice-group/TeBaQA
#  algorithms details: https://github.com/dice-group/TeBaQA/blob/master/TeBaQA_appendix.pdf
#  Query types & ASC & DESC are hardcoded: https://github.com/dice-group/TeBaQA/blob/master/nlp/src/main/java/de/uni/leipzig/tebaqa/nlp/core/NLPAnalyzerEnglish.java
#
# QUERY = "Who was the doctoral supervisor of Albert Einstein?"
# QUERY = "Who was the doctoral mentor of Einstein?"

# # FIXME: how many
# QUERY = "How many children did Benjamin Franklin have?"
# QUERY = "In which UK city are the headquarters of the MI6?"
# QUERY = "what's the news"

# TODO: test: WDAqua-core1
# QUERY = "Give me actors born in Strasbourg"
# QUERY = "actors born in Strasbourg"
# QUERY = "actors Strasbourg born in"
# QUERY = "born actor Strasbourg"

# TODO: AskNow
# QUERY = "Which country is California located in?"  # FIXME:
# QUERY = "Which artists where born on the same date as Rachel Stevens?"  # FIXME:
# QUERY = "New York is located in which country?"  # FIXME:
# QUERY = "Which is the country where New York is located?"  # OK
# QUERY = "In which country is New York located?"  # FIXME:


# TODO: Gerbil for QA platform
#  !!! http://gerbil-qa.aksw.org/gerbil/ => ofera date statistice pentru o serie de QA systems
#  https://github.com/dice-group/gerbil => github repo
#  https://github.com/dice-group/gerbil/wiki/Question-Answering#web-service-interface => formatul acceptat de Gerbil
# Usbeck,R.,Röder,M.,Hoffmann,M.,Conrads,F.,Huthmann,J.,Ngonga-Ngomo,
# A.C., Demmler, C., Unger, C.: Benchmarking question answering systems. Se-
# mantic Web Journal (2016), to appear















# interrogative pronouns: who, what, which, whose

# TODO: get_subject_entities => brother in law = compound noun
QUERY = "My brother in law was there"

# relative pronouns: who, that, which
# who => relative pronoun linking "my sister" to "21 years old"
QUERY = "I go with my sister who is 21 years old"

# half-time = compound noun
QUERY = "At half-time of football"




QUERY = "Which school did Robbie Diack attend?"  # FIXME
QUERY = "Where is the successor of john waldo from?"  # FIXME
QUERY = "What is the birth city of trainer of Leallah?"  # FIXME
QUERY = "What is the genre of the Band whose home town is County Westmeath?"  # FIXME
QUERY = "What is Bob Adams (American football) known for?"  # FIXME
QUERY = "What is the mascot of military in Quezon city?"  # TODO
QUERY = "Which country does league of Nguendula Filipe belongs to?"  # FIXME
QUERY = "Where is the senator from whose successor was James belford?"  # FIXME
QUERY = "Which comic characters are painted by Bill Finger?"  # TODO
QUERY = " Which musical band produced the subsequent work of City of New Orleans ?"  # FIXME: list(sentence.noun_chunks) == []
QUERY = "Who is the singer born in 1993?"  # FIXME https://sci-hub.se/10.1007/s10844-019-00589-2


QUERY = "How many pages does War and Peace have?"
QUERY = "What is the official color of the University of Oxford?"

QUERY = "Who is the wife of Donald Trump?"
QUERY = "Where in France is sparkling wine produced?"
QUERY = "What is the time zone of Salt Lake City?"


# https://github.com/KGQA/QALD-10/blob/main/data/qald_10/qald_10.json
QUERY = "What is the Fujiyama made of?"
QUERY = "Where does the Granny Smith apple variety come from?"
QUERY = "Where are the founders of the band Metallica from?"
QUERY = "Who founded the architectural firm who planned the Elbphilharmonie?"
QUERY = "What percentage of Andorra is covered with water?"
QUERY = "What is the area of the capital of Spitsbergen?"
QUERY = "What is the twitter name of Running Wild?"
QUERY = "Where is the poet Alexander Pope buried?"
QUERY = "What is native name of the composer of the Japanese national anthem?"
QUERY = "Who is the founder of the capital of Vietnam?"
QUERY = "What is the area of the Great Lakes?"  # original: "What is the area of the great lakes?"


# https://github.com/KGQA/QALD_9_plus/blob/main/data/qald_9_plus_test_dbpedia.json
QUERY = "Who killed Caesar?"
QUERY = "What is the highest mountain in Germany?"
QUERY = "Which instruments does Cat Stevens play?"
QUERY = "Which book has the most pages?"
QUERY = "What is the largest state in the United States?"


# https://github.com/mllovers/geo880-sparql/blob/master/geo-880.en
# https://arxiv.org/pdf/1803.04329.pdf
QUERY = "which state has the smallest population density?"
# QUERY = QUERY_01


# https://arxiv.org/html/1708.07624
# https://github.com/BaiBlanc/neural-qa/tree/master/data



# https://github.com/pkumod/gAnswer/blob/master/src/qa/parsing/BuildQueryGraph.java

# [2019] https://dl.gi.de/handle/20.500.12116/21702
# [2019] https://ieeexplore.ieee.org/abstract/document/9627128
# [2014] https://ceur-ws.org/Vol-1180/CLEF2014wn-QA-Dima2014.pdf


# TODO: https://github.com/ag-sc/QALD/blob/master/5/data/qald-5_train.json


QUERY = "What is the time zone of Salt Lake City?"
QUERY = "Which of the volcanoes that erupted in 1550 is still active?"

QUERY = "Where Gregory I at Byzantine Empire dired?"  # FIXME: "Gregory I at Byzantine Empire"
QUERY = "Was Alexis of Russia was born at Tsardom of Russia?"  # FIXME: "Alexis of Russia" & "Tsardom of Russia"
