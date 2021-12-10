import spacy
import requests
from spacy import displacy

from nltk.corpus import wordnet
from ro.webdata.oniq.model.rdf.SimilarityMap import SimilarityMap

from ro.webdata.oniq.common.constants import GLOBAL_ENV, TEST_MODES
from ro.webdata.oniq.model.sparql.MetaQuery import MetaQuery
from ro.webdata.oniq.nlp.statements import get_statement_list
from ro.webdata.oniq.validation.dataset.dataset import PAIRS
from ro.webdata.oniq.validation.tests import question_statement_test, question_statements_test
from ro.webdata.oniq.nlp.word_utils import is_wh_word

import logging
import sys

ENDPOINT = "http://localhost:7200/repositories/TESTING_BCU_CLUJ"
ENDPOINT = "http://localhost:7200/repositories/eCHO"

nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en_core_web_md')

QUERY = "Which paintings are not located in Bacau?"
if GLOBAL_ENV.TEST_MODE == TEST_MODES.DEFAULT:
    sparql_query = MetaQuery(ENDPOINT, QUERY)
elif GLOBAL_ENV.TEST_MODE == TEST_MODES.LOCAL_TEST:
    document = nlp(QUERY)
    statements = get_statement_list(document)
    question_statement_test(document.text, statements, PAIRS)

    # nlp_query = nlp(QUERY)
    # displacy.serve(nlp_query, style="dep")
else:
    question_statements_test(nlp, PAIRS)


# # https://blog.einstein.ai/how-to-talk-to-your-database/
# rdf_utils.parse_rdf("../../../../files/input/rdf/demo_2.rdf")


# from ro.webdata.nqi.rdf.Match import Match
# from ro.webdata.nqi.rdf import rdf_utils
# match = Match(ENDPOINT, ['location'])
# print('location:', match)
