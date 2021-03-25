from ro.webdata.oniq.common.print_const import COLORS
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.test.dataset import pairs


def question_statements_test(question: str, statements: [Statement]):
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
        else:
            print(f'{COLORS.LIGHT_RED}TEST FAILED:\n'
                  f'\tmessage: The statements have been MODIFIED!\n'
                  f'\tquestion: "{question}"{COLORS.RESET_ALL}')
    else:
        print(f'{COLORS.LIGHT_YELLOW}TEST NOT COMPLETED:\n'
              f'\tmessage: The question is not part of the current test dataset!\n'
              f'\tquestion: "{question}"{COLORS.RESET_ALL}')
    print()

    return statements


def _prepare_statements_str(statements: [Statement]):
    statements_str = "\n"
    for statement in statements:
        statements_str += statement.get_basic_str() + "\n\n"
    return statements_str
