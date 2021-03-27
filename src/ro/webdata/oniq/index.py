import spacy

from ro.webdata.oniq.common.constants import GLOBAL_ENV, TEST_MODES
from ro.webdata.oniq.model.sparql.MetaQuery import MetaQuery
from ro.webdata.oniq.nlp.statements import get_statement_list
from ro.webdata.oniq.test.dataset import pairs
from ro.webdata.oniq.test.tests import question_statement_test, question_statements_test

ENDPOINT = "http://localhost:7200/repositories/TESTING_BCU_CLUJ"
ENDPOINT = "http://localhost:7200/repositories/eCHO"


nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5')
# nlp = spacy.load('../../../../lib/en_core_web_md/en_core_web_md-2.2.5')

QUERY = 'Which paintings are not located in Bacau?'
if GLOBAL_ENV.TEST_MODE == TEST_MODES.DEFAULT:
    sparql_query = MetaQuery(ENDPOINT, QUERY)
elif GLOBAL_ENV.TEST_MODE == TEST_MODES.LOCAL_TEST:
    document = nlp(QUERY)
    statements = get_statement_list(document)
    question_statement_test(document.text, statements, pairs)
else:
    question_statements_test(nlp, pairs)


# # https://blog.einstein.ai/how-to-talk-to-your-database/
# rdf_utils.parse_rdf("../../../../files/input/rdf/demo_2.rdf")


# from ro.webdata.nqi.rdf.Match import Match
# from ro.webdata.nqi.rdf import rdf_utils
# match = Match(ENDPOINT, 'location')
# print('location:', match)


