from ro.webdata.nqi.common.constants import STR_SEPARATOR


class Triple:
    def __init__(self, s: [str] = None, p: str = None, o: str = None):
        self.s = s
        self.p = p
        self.o = o

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}{{ <{STR_SEPARATOR.join(self.s)}> <{self.p}> <{self.o}> }}'
        )
