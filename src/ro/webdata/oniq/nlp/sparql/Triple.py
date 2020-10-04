from ro.webdata.oniq.common.constants import VARIABLE_PREFIX, VARIABLE_SEPARATOR


class Triple:
    def __init__(self, s: str = None, p: str = None, o: str = None):
        self.s = s
        self.p = p
        self.o = o

    def __str__(self):
        return self.get_str()

    def __eq__(self, other):
        if not isinstance(other, Triple):
            return NotImplemented
        return self.s == other.s and self.p == other.p and self.o == other.o

    def get_str(self, indentation=''):
        return (
            f'{indentation}{{ <{self.s}> <{self.p}> <{self.o}> }}'
        )

    def get_triple_pattern(self, indentation='\t'):
        return (
            f'{indentation}'
            f'{VARIABLE_PREFIX}{self.s}{VARIABLE_SEPARATOR}'
            f'{self.p}{VARIABLE_SEPARATOR}'
            f'{VARIABLE_PREFIX}{self.o}{VARIABLE_SEPARATOR}'
        )
