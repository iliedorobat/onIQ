from ro.webdata.oniq.common.constants import VARIABLE_PREFIX, VARIABLE_SEPARATOR


class Target:
    def __init__(self, name: str, values: [] = None, stmt_type=None):
        self.name = name
        self.values = values if values is not None else []
        self.stmt_type = stmt_type

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        values = [token.text for token in self.values]
        return (
            f'{indentation}{{ {self.name}: {", ".join(values)} : {self.stmt_type } }}'
        )

    def get_variable_pattern(self, indentation=''):
        return (
            f'{indentation}'
            f'{VARIABLE_PREFIX}{self.name}{VARIABLE_SEPARATOR}'
        )
