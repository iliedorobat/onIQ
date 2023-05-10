from ro.webdata.oniq.common.constants import GLOBAL_ENV, TEST_MODES
from ro.webdata.oniq.sparql.builder import SPARQLBuilder
from ro.webdata.oniq.validation.validation.pairs import PAIRS
from ro.webdata.oniq.validation.validation.pairs_qald_5_test import PAIRS_QALD
from ro.webdata.oniq.validation.validation.test import question_test, questions_test


ENDPOINT = "http://localhost:7200/repositories/TESTING_BCU_CLUJ"
ENDPOINT = "http://localhost:7200/repositories/eCHO"

QUERY = "Who were the parents of Queen Victoria?"  # OK

if GLOBAL_ENV.TEST_MODE == TEST_MODES.DEFAULT:
    sparql_query = SPARQLBuilder(ENDPOINT, QUERY)
elif GLOBAL_ENV.TEST_MODE == TEST_MODES.LOCAL_TEST:
    question_test(PAIRS_QALD, QUERY, True, True, True)
    questions_test(PAIRS_QALD, True, False, True)

    questions_test(PAIRS_QALD, False, False, False)
    questions_test(PAIRS, False, False, False)
else:
    questions_test(PAIRS_QALD, True, False, False)
    questions_test(PAIRS, False, False, False)

# displacy.serve(nlp_query, style="dep")
