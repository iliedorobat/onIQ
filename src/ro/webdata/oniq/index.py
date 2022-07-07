import spacy

from ro.webdata.oniq.common.constants import GLOBAL_ENV, TEST_MODES
from ro.webdata.oniq.nlp.stmt_utils import get_statement_list
from ro.webdata.oniq.sparql.builder import SPARQLBuilder
from ro.webdata.oniq.validation.dataset.dataset import PAIRS
from ro.webdata.oniq.validation.tests import question_statement_test, question_statements_test

ENDPOINT = "http://localhost:7200/repositories/TESTING_BCU_CLUJ"
ENDPOINT = "http://localhost:7200/repositories/eCHO"

nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en_core_web_md')

QUERY = "Which paintings are not located in Bacau?"

if GLOBAL_ENV.TEST_MODE == TEST_MODES.DEFAULT:
    sparql_query = SPARQLBuilder(ENDPOINT, QUERY)
elif GLOBAL_ENV.TEST_MODE == TEST_MODES.LOCAL_TEST:
    document = nlp(QUERY)
    statements = get_statement_list(document)
    question_statement_test(document.text, statements, PAIRS)

    # nlp_query = nlp(QUERY)
    # displacy.serve(nlp_query, style="dep")
else:
    question_statements_test(nlp, PAIRS)

print(QUERY)
