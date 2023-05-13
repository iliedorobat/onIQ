from ro.webdata.oniq.common.constants import GLOBAL_ENV
from ro.webdata.oniq.common.print_utils import COLORS

from ro.webdata.oniq.sparql.builder import SPARQLBuilder


ENDPOINT = "http://localhost:7200/repositories/TESTING_BCU_CLUJ"
ENDPOINT = "http://localhost:7200/repositories/eCHO"


class RESULT_TYPES:
    PASSED = "passed"
    FAILED = "failed"
    NO_COMPLETED = "not_completed"


def questions_test(pairs, print_summary, print_deps, print_result):
    counter = {
        RESULT_TYPES.PASSED: 0,
        RESULT_TYPES.FAILED: 0,
        RESULT_TYPES.NO_COMPLETED: 0
    }

    for pair in pairs:
        result = question_test(pairs, pair["query"], print_summary, print_deps, print_result)

        if result == RESULT_TYPES.PASSED:
            counter[RESULT_TYPES.PASSED] += 1
        elif result == RESULT_TYPES.FAILED:
            counter[RESULT_TYPES.FAILED] += 1
        elif result == RESULT_TYPES.NO_COMPLETED:
            counter[RESULT_TYPES.NO_COMPLETED] += 1

    print(
        f'\n'

        f'{COLORS.LIGHT_CYAN}'
        f'PASSED: {counter["passed"]}'
        f'{COLORS.RESET_ALL}\n'

        f'{COLORS.LIGHT_RED}'
        f'FAILED: {counter["failed"]}'
        f'{COLORS.RESET_ALL}\n'

        f'{COLORS.LIGHT_YELLOW}'
        f'NOT COMPLETED: {counter["not_completed"]}'
        f'{COLORS.RESET_ALL}\n'
    )


def question_test(pairs, question: str, print_summary, print_deps, print_result):
    sparql = SPARQLBuilder(ENDPOINT, question, print_deps, print_result)
    exists = False
    is_equal = False

    for pair in pairs:
        if question.lower() == pair["query"].lower():
            exists = True
            is_equal = str(sparql.raw_query).strip().lower() == pair["result"].strip().lower()
            break

    if exists:
        if is_equal:
            if GLOBAL_ENV.IS_DEBUG and print_summary:
                print(f'{COLORS.LIGHT_CYAN}TEST PASSED\n'
                      f'\tmessage: The statements have not been modified!\n'
                      f'\tquestion: "{question}"{COLORS.RESET_ALL}')
            return RESULT_TYPES.PASSED
        else:
            if GLOBAL_ENV.IS_DEBUG and print_summary:
                print(f'{COLORS.LIGHT_RED}TEST FAILED:\n'
                      f'\tmessage: The statements have been MODIFIED!\n'
                      f'\tquestion: "{question}"{COLORS.RESET_ALL}')
            return RESULT_TYPES.FAILED
    else:
        if GLOBAL_ENV.IS_DEBUG and print_summary:
            print(f'{COLORS.LIGHT_YELLOW}TEST NOT COMPLETED:\n'
                  f'\tmessage: The question is not part of the current test dataset!\n'
                  f'\tquestion: "{question}"{COLORS.RESET_ALL}')
        return RESULT_TYPES.NO_COMPLETED
