from ro.webdata.oniq.common.print_const import COLORS
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.nlp.statements import get_statement_list


class RESULT_TYPES:
    PASSED = "passed"
    FAILED = "failed"
    NO_COMPLETED = "not_completed"


def question_statements_test(nlp, pairs):
    counter = {
        RESULT_TYPES.PASSED: 0,
        RESULT_TYPES.FAILED: 0,
        RESULT_TYPES.NO_COMPLETED: 0
    }

    for pair in pairs:
        document = nlp(pair["query"])
        statements = get_statement_list(document)
        result = question_statement_test(pair["query"], statements, pairs)

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


def question_statement_test(question: str, statements: [Statement], pairs):
    statements_str = _prepare_statements_str(statements)

    exists = False
    is_equal = False

    for pair in pairs:
        if question == pair["query"]:
            exists = True
            is_equal = statements_str.strip() == pair["result"].strip()
            break

    if exists:
        if is_equal:
            print(f'{COLORS.LIGHT_CYAN}TEST PASSED\n'
                  f'\tmessage: The statements have not been modified!\n'
                  f'\tquestion: "{question}"{COLORS.RESET_ALL}')
            return RESULT_TYPES.PASSED
        else:
            print(f'{COLORS.LIGHT_RED}TEST FAILED:\n'
                  f'\tmessage: The statements have been MODIFIED!\n'
                  f'\tquestion: "{question}"{COLORS.RESET_ALL}')
            return RESULT_TYPES.FAILED
    else:
        print(f'{COLORS.LIGHT_YELLOW}TEST NOT COMPLETED:\n'
              f'\tmessage: The question is not part of the current test dataset!\n'
              f'\tquestion: "{question}"{COLORS.RESET_ALL}')
        return RESULT_TYPES.NO_COMPLETED


def _prepare_statements_str(statements: [Statement]):
    statements_str = "\n"
    for statement in statements:
        statements_str += statement.get_basic_str() + "\n"
    return statements_str
