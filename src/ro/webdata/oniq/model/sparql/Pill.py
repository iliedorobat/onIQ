from ro.webdata.oniq.common.constants \
    import COMPARISON_OPERATORS, LOGICAL_OPERATORS, PREFIX, SEPARATOR


class Pill:
    def __init__(self, key: str = None, negation: str = None, operator=None, value: str = None):
        self.key = key
        self.operator = operator
        self.value = value
        # self.logical_operation = logical_operation
        self.negation = negation

    def __str__(self):
        return self.get_str('\t\t')

    def get_str(self, indentation=''):
        # logical_operation = f'[{self.logical_operation}]' if self.logical_operation.name is not None else '[]'
        key = f'<{self.key}>'
        operator = f'<{self.operator}>'
        value = f'<{self.value}>'

        return (
            # f'{indentation}{{ {logical_operation} {key} {operator} {value} }}'
            f'{indentation}{{ {key} {operator} {value} }}'
        )

    def get_pill_pattern(self, indentation='\t'):
        variable = f'{PREFIX.VARIABLE}{self.key}'
        return (
            f'{indentation}'
            f'{_get_operand(variable, True, True)}{SEPARATOR.TRIPLE_PATTERN}'
            f'{_get_operator(self)}{SEPARATOR.TRIPLE_PATTERN}'
            f'{_get_operand(self.value, False, True)}'
        )


class Pills:
    def __init__(self, targets: [Pill] = None, conditions: [Pill] = None):
        self.targets = targets if targets is not None else []
        self.conditions = conditions if conditions is not None else []

    def __str__(self):
        return self.get_str()

    # TODO: print the conditions
    def get_str(self, indentation='\t'):
        targets_str = '{'
        targets_str += f'\n{indentation}{indentation}target pills: ['

        for target in self.targets:
            targets_str += f'\n{indentation}' + str(target)

        targets_str += f'\n{indentation}{indentation}]' if len(self.targets) > 0 else ']'
        targets_str += f'\n{indentation}'

        return targets_str

    def get_target_pills_pattern(self, indentation='\t\t'):
        statement = ''

        for i in range(0, len(self.targets)):
            pill = self.targets[i]
            statement += pill.get_pill_pattern(indentation) + SEPARATOR.TRIPLE_PATTERN
            statement += LOGICAL_OPERATORS.OR + '\n' if i < len(self.targets) - 1 else ''

        return statement.rstrip()

    # TODO:
    def get_conditions_pills_pattern(self, indentation='\t\t'):
        return ''


def _get_operator(pill: Pill):
    if pill.negation is not None:
        if pill.operator == COMPARISON_OPERATORS.CONTAINS:
            return COMPARISON_OPERATORS.NOT_CONTAINS
        if pill.operator == COMPARISON_OPERATORS.EQ:
            return COMPARISON_OPERATORS.NOT_EQ
    return pill.operator


def _get_operand(operand, is_variable=False, is_sensitive=False):
    value = operand if is_variable else f'"{operand}"'
    return f'{value}' if not is_sensitive else f'lcase({value})'
