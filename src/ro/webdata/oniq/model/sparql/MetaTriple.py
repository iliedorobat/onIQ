from ro.webdata.oniq.model.sparql.Filter import Filter
from ro.webdata.oniq.model.sparql.Pill import Pill
from ro.webdata.oniq.model.sparql.Triple import Triple


class MetaTriple:
    def __init__(self, triple: Triple = None, pills: [Pill] = None):
        self.triple: Triple = triple
        self.filter = Filter(pills)

    def __str__(self):
        return self.get_str()

    def get_pills(self):
        pills_str = ''

        for i in range(0, len(self.pills.targets)):
            pill = self.pills.targets[i]
            pills_str += '\n' if i < len(self.pills.targets) - 1 else ''
            pills_str += str(pill)

        return pills_str

    def get_str(self, indentation=''):
        return (
            f'{indentation}meta triple: {{\n'
            f'{indentation}\ttriple: {Triple.get_str(self.triple)},\n'
            f'{indentation}\tpill: {self.pills}\n'
            f'{indentation}}}'
        )
