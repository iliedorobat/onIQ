from ro.webdata.oniq.common.constants import PREFIX, SEPARATOR
from ro.webdata.oniq.model.rdf.Property import Property


class Triple:
    def __init__(self, target_name: str = None, prop: Property = None):
        self.s = target_name
        self.p = prop.prop_name_extended if prop is not None else None
        self.o = prop.prop_name_extended.replace(SEPARATOR.NAMESPACE, SEPARATOR.STRING) if prop is not None else None

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
            f'{PREFIX.VARIABLE}{self.s}{SEPARATOR.TRIPLE_PATTERN}'
            f'{self.p}{SEPARATOR.TRIPLE_PATTERN}'
            f'{PREFIX.VARIABLE}{self.o}{SEPARATOR.TRIPLE_PATTERN}'
        )
