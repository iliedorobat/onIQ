from ro.webdata.nqi.nlp.sentence.constants import TYPE_SELECT_CLAUSE, TYPE_WHERE_CLAUSE
from ro.webdata.nqi.rdf import parser
from ro.webdata.nqi.rdf.Match import Match


# TODO: split the Query.py file
class Query:
    def __init__(self, endpoint, statements):
        self.targets = _get_targets(statements)
        self.meta_triples = _get_meta_triples(endpoint, statements, self.targets)

    @staticmethod
    def get_prefixes(endpoint):
        namespaces = parser.get_namespaces(endpoint)
        prefixes = ''

        for i in range(len(namespaces)):
            namespace = namespaces[i]
            left_space = '\n' if i > 0 else ''
            prefixes += f'{left_space}PREFIX {namespace.label}: <{namespace.name}>'

        return prefixes

    def get_targets_str(self):
        targets_str = ''

        for i in range(len(self.targets)):
            targets_str += f'?{self.targets[i].lemma_}'
            targets_str += ' ' if i < len(self.targets) - 1 else ''

        return targets_str

    def get_where_block(self):
        triples_str = ''

        for i in range(len(self.meta_triples)):
            meta_triple = self.meta_triples[i]
            conjunction = meta_triple.conjunction.text.upper() if meta_triple.conjunction is not None else None

            # TODO: OR
            if conjunction is None or conjunction == 'AND':
                if conjunction == 'AND':
                    triples_str += ' .\n'
                triples_str += f'?{meta_triple.triple.s} {meta_triple.triple.p} ?{meta_triple.triple.o}'

        return triples_str

    def get_filter_block(self):
        filter_str = ''

        for i in range(len(self.meta_triples)):
            meta_triple = self.meta_triples[i]
            filter_str += str(meta_triple.filter_clause)
            filter_str += '.\n' if i < len(self.targets) - 1 else ''

        return filter_str

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        meta_triples_str = ""
        tab = '\t\t'

        for i in range(len(self.meta_triples)):
            meta_triple = self.meta_triples[i]
            meta_triples_str += f'{indentation}{meta_triple.get_str(tab)}'
            meta_triples_str += ',\n' if i < len(self.meta_triples) - 1 else ''

        return (
            f'{indentation}query: {{\n'
            f'{indentation}\ttargets: {self.targets},\n'
            f'{indentation}\tmeta triples: [\n'
            f'{indentation}{meta_triples_str}\n'
            f'{indentation}\t]\n'
            f'{indentation}}}'
        )


class MetaTriple:
    def __init__(self, s=None, p=None, o=None, value=None, negation=None, conjunction=None, stmt_type=None):
        self.triple = Triple(s, p, o)
        self.value = value
        self.negation = negation
        self.conjunction = conjunction
        self.filter_clause = None

        if stmt_type == TYPE_SELECT_CLAUSE:
            query_filter = _Filter(_FILTER_OPERATORS.CONTAINS, self.triple.o, self.value)
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


class Triple:
    def __init__(self, s=None, p=None, o=None):
        self.s = s
        self.p = p
        self.o = o

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}{{ <{self.s}> <{self.p}> <{self.o}> }}'
        )


class _Filter:
    def __init__(self, operator, obj, constraint):
        self.operator = operator
        self.obj = obj
        self.constraint = constraint

    def __str__(self):
        filter_str = 'FILTER({statement})'

        # TODO: implement the REGEX operator
        if self.operator in [_FILTER_OPERATORS.CONTAINS, _FILTER_OPERATORS.NOT_CONTAINS]:
            filter_str = filter_str.format(statement=f'{self.operator}(?{self.obj}, "{self.constraint}")')
        elif self.operator in [_FILTER_OPERATORS.EQ, _FILTER_OPERATORS.NOT_EQ, _FILTER_OPERATORS.GT, _FILTER_OPERATORS.GTE, _FILTER_OPERATORS.LT, _FILTER_OPERATORS.LTE]:
            filter_str = filter_str.format(statement=f'?{self.obj} {self.operator} "{self.constraint}"')
        else:
            filter_str = ''

        return filter_str


class _FILTER_OPERATORS:
    CONTAINS = 'contains'
    NOT_CONTAINS = '!contains'
    REGEX = 'regex'
    EQ = '='
    NOT_EQ = '!='
    GT = '>'
    GTE = '>='
    LT = '<'
    LTE = '<='


def _get_targets(statements):
    targets = []

    for stmt in statements:
        if stmt.type == TYPE_SELECT_CLAUSE:
            stmt_targets = [
                token for token in stmt.phrase
                if token.pos_ == "NOUN" and token.tag_ in ["NN", "NNS"]
            ]
            targets = targets + stmt_targets

    return targets


def _get_meta_triples(endpoint, statements, targets):
    triples = []

    for stmt in statements:
        verb_stmt = stmt.action.verb_stmt
        verb = verb_stmt.main_vb \
            if verb_stmt.main_vb is not None \
            else verb_stmt.aux_vb
        negation = verb_stmt.neg
        conjunction = stmt.conjunction
        noun_list = [token for token in stmt.phrase if token.pos_ == "NOUN"]

        for target in targets:
            prop = _get_matched_property(endpoint, verb)
            triple_s = target.lemma_
            triple_p = prop.prop_name_extended if prop is not None else None
            triple_o = prop.prop_name_extended.replace(':', '_') if prop is not None else None

            if stmt.type == TYPE_SELECT_CLAUSE:
                pobj_tokens = [token for token in stmt.phrase if token.dep_ == "pobj"]
                for token in pobj_tokens:
                    triples.append(MetaTriple(triple_s, triple_p, triple_o, token.text, negation, conjunction, stmt.type))
            elif stmt.type == TYPE_WHERE_CLAUSE:
                for noun in noun_list:
                    triples.append(MetaTriple(triple_s, triple_p, triple_o, noun.text, negation, conjunction))

    return triples


def _get_matched_property(endpoint, verb):
    properties = parser.get_properties(endpoint)
    match = Match(endpoint, verb.text)

    # TODO: add support for all properties from "matched" set
    for prop in properties:
        for matched in match.matched:
            if prop.prop_name == matched:
                return prop

    return None


def _get_triple_predicate(endpoint, verb):
    properties = parser.get_properties(endpoint)
    match = Match(endpoint, verb.text)
    predicate = None

    # TODO: add support for all properties in the "matched" set
    for prop in properties:
        for matched in match.matched:
            if prop.prop_name == matched:
                predicate = prop.prop_name_extended

    return predicate
