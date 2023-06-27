import warnings

from ro.webdata.oniq.common.constants import GLOBAL_ENV, TEST_MODES
from ro.webdata.oniq.sparql.builder.builder import SPARQLBuilder
from ro.webdata.oniq.validation.pre_validation_pairs.pairs import PAIRS
from ro.webdata.oniq.validation.validation import questions_test, question_test
from ro.webdata.oniq.validation.validation_pairs.pairs_qald_5_test import PAIRS_QALD as V_PAIRS_QALD, PAIRS_QALD

# Ignore spaCy "[W008] Evaluating Token.similarity based on empty vectors." warning message
warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)

ENDPOINT = "http://localhost:7200/repositories/TESTING_BCU_CLUJ"
ENDPOINT = "http://localhost:7200/repositories/eCHO"

QUERY_01 = "Did Arnold Schwarzenegger attend a university?"  # OK
QUERY_02 = "Is Barack Obama a democrat?"  # OK
QUERY_03 = "In which country is Mecca located?"  # OK
QUERY_04 = "Give me all ESA astronauts."  # TODO:
QUERY_05 = "Give me all Swedish holidays."  # OK
QUERY_06 = "Give me the currency of China."  # OK
QUERY_07 = "When did the Ming dynasty dissolve?"  # OK
QUERY_08 = "Who is the manager of Real Madrid?"  # OK
QUERY_09 = "Who were the parents of Queen Victoria?"  # OK
QUERY_10 = "Who is the youngest Pulitzer Prize winner?"  # OK
QUERY_11 = "Who is the oldest child of Meryl Streep?"  # TODO: reverse
QUERY_12 = "Who is the tallest basketball player?"  # OK
QUERY_13 = "What is the net income of Apple?"  # OK
QUERY_14 = "What is the highest mountain in Italy?"  # OK
QUERY_15 = "How high is the Yokohama Marine Tower?"  # OK
QUERY_16 = "How many ethnic groups live in Slovenia?"  # TODO: reverse
QUERY_17 = "Which soccer players were born on Malta?"  # OK
QUERY_18 = "Which museum in New York has the most visitors?"  # OK
QUERY_19 = "How many companies were founded by the founder of Facebook?"  # OK ===
QUERY_20 = "Give me all Swiss non-profit organizations."  # OK ...
QUERY_21 = "Which musician wrote the most books?"  # OK ...
QUERY_22 = "Which volcanos in Japan erupted since 2000?"  # TODO:

QUERY_LIST = [
    QUERY_01, QUERY_02, QUERY_03, QUERY_04, QUERY_05,
    QUERY_06, QUERY_07, QUERY_08, QUERY_09, QUERY_10,
    QUERY_11, QUERY_12, QUERY_13, QUERY_14, QUERY_15,
    QUERY_16, QUERY_17, QUERY_18, QUERY_19, QUERY_20,
    QUERY_21, QUERY_22,
]

print_summary = True
print_deps = True
raw_test = False

QUERY = QUERY_LIST[0]
# question_test(PAIRS_QALD, QUERY, True, print_summary, print_deps)
# question_test(V_PAIRS_QALD, QUERY, False, print_summary, print_deps)

# print("Validating Raw SPARQL Queries...\n")
# questions_test(PAIRS_QALD, True, print_summary, print_deps)
# questions_test(PAIRS, True, print_summary, print_deps)

print("Validating Final SPARQL Queries...\n")
questions_test(V_PAIRS_QALD, False, True, True)

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
