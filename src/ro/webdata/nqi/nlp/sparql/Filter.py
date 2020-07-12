from ro.webdata.nqi.common.constants import VARIABLE_PREFIX
from ro.webdata.nqi.common.operators import COMPARISON_OPERATORS, MATH_OPERATORS


class Filter:
    def __init__(self, operator, obj, constraints):
        self.operator = operator
        self.obj = obj
        self.constraints = constraints

    def __str__(self, is_sensitive=False):
        filter_str = 'FILTER({statement})'

        # TODO: implement the REGEX operator
        if self.operator in [
            COMPARISON_OPERATORS.CONTAINS,
            COMPARISON_OPERATORS.NOT_CONTAINS
        ]:
            # TODO: check if len(constraints) > 0
            statement = f'{_generate_contains_clause(self.operator, self.obj, self.constraints, is_sensitive)}'
            filter_str = filter_str.format(statement=statement)
        elif self.operator in [
            COMPARISON_OPERATORS.EQ,
            COMPARISON_OPERATORS.NOT_EQ,
            COMPARISON_OPERATORS.GT,
            COMPARISON_OPERATORS.GTE,
            COMPARISON_OPERATORS.LT,
            COMPARISON_OPERATORS.LTE
        ]:
            # TODO: check if len(constraints) == 1
            variable = _get_variable(self.obj)
            statement = f'{variable} {self.operator} "{self.constraints[0]}"'
            filter_str = filter_str.format(statement=statement)
        else:
            filter_str = ''

        return filter_str


def _generate_contains_clause(operator, obj, constraints, is_sensitive):
    clause = None

    for i in range(len(constraints)):
        constraint = constraints[i]
        variable = _get_variable(obj)
        sens_constraint = _get_sens_operand(constraint, is_sensitive)

        if i == 0:
            clause = f'{operator}({variable}, {sens_constraint})'
        else:
            clause += f' {MATH_OPERATORS.OR} {operator}({variable}, {sens_constraint})'

    return clause


def _get_sens_operand(operand, is_sensitive=False):
    return f'"{operand}"' if is_sensitive else f'lcase("{operand}")'


# TODO: move the method into utils (it's also used in Query.py)
def _get_variable(var_name):
    return f'{VARIABLE_PREFIX}{var_name}'
