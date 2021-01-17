from spacy.tokens import Span, Token
from ro.webdata.oniq.common.constants import LOGICAL_OPERATIONS


# TODO: documentation
class LogicalOperation:
    def __init__(self, sentence: Span, value: Span):
        self.name = _get_operation_name(sentence, value)
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, LogicalOperation):
            return NotImplemented
        return other is not None and \
            self.name == other.name and \
            self.value == other.value

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        name = self.name if self else None

        return (
            f'{indentation}logical operation: {name}'
        )


def _get_operation_name(sentence: Span, chunk: Span):
    first_index = chunk[0].i

    if first_index > 0:
        prev_word = sentence[first_index - 1]
        return _map_operation_name(prev_word)

    return None


def _map_operation_name(token: Token):
    operation = token.lower_
    if operation in [',', 'and']:
        return LOGICAL_OPERATIONS.AND
    if operation == 'or':
        return LOGICAL_OPERATIONS.OR
    return None
