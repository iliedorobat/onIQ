from ro.webdata.oniq.nlp.sentence.constants import TYPE_SELECT_CLAUSE
from ro.webdata.oniq.nlp.sparql.Filter import Filter, COMPARISON_OPERATORS
from ro.webdata.oniq.nlp.sparql.Triple import Triple


class MetaTriple:
    def __init__(self, triple: Triple = None, value: [str] = None, negation=None, conjunction=None, stmt_type=None):
        self.triple: Triple = triple
        self.value = value
        self.negation = negation
        self.conjunction = conjunction
        self.filter_clause = None
        self.def_filter_clause(stmt_type)

    def def_filter_clause(self, stmt_type):
        if stmt_type == TYPE_SELECT_CLAUSE:
            query_filter = Filter(COMPARISON_OPERATORS.CONTAINS, self.triple.o, self.value)
            self.filter_clause = str(query_filter)

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}meta triple: {{\n'
            f'{indentation}\ttriple: {Triple.get_str(self.triple)},\n'
            f'{indentation}\tvalue: {self.value}\n'
            f'{indentation}\tnegation: {self.negation}\n'
            f'{indentation}\tconjunction: {self.conjunction}\n'
            f'{indentation}\tfilter_clause: {self.filter_clause}\n'
            f'{indentation}}}'
        )
