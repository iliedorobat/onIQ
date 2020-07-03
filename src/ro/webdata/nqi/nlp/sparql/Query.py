from ro.webdata.nqi.nlp.sentence.constants import TYPE_SELECT_CLAUSE, TYPE_WHERE_CLAUSE


class Query:
    def __init__(self, statements):
        self.targets = _get_targets(statements)
        self.meta_triples = _get_meta_triples(statements, self.targets)

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
            f'{indentation}\ttargets: {self.targets}\n'
            f'{indentation}\tmeta triples: [\n'
            f'{indentation}{meta_triples_str}\n'
            f'{indentation}\t]\n'
            f'{indentation}}}'
        )


class MetaTriple:
    def __init__(self, s=None, p=None, o=None, negation=None):
        self.triple = Triple(s, p, o)
        self.negation = negation

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}meta triple: {{\n'
            f'{indentation}\ttriple: {Triple.get_str(self.triple)}\n'
            f'{indentation}\tnegation: {self.negation}\n'
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
            f'{{ <{self.s}> <{self.p}> <{self.o}> }}'
        )


def _get_targets(statements):
    targets = []

    for stmt in statements:
        if stmt.type == TYPE_SELECT_CLAUSE:
            stmt_targets = [
                token for token in stmt.phrase
                # TODO: "which is the largest museum which hosts more than 10 pictures and exposed one sword?"
                # if token.pos_ == "NOUN" and token.dep_ in ["nsubj", "nsubjpass", "conj", "attr"]
                if token.pos_ == "NOUN" and token.tag_ == "NN"
            ]
            targets = targets + stmt_targets

    return targets


def _get_meta_triples(statements, targets):
    triples = []

    for stmt in statements:
        if stmt.type == TYPE_WHERE_CLAUSE:
            verb_stmt = stmt.action.verb_stmt
            verb = verb_stmt.main_vb \
                if verb_stmt.main_vb is not None \
                else verb_stmt.aux_vb
            negation = verb_stmt.neg
            noun_list = [token for token in stmt.phrase if token.pos_ == "NOUN"]

            for target in targets:
                for noun in noun_list:
                    triples.append(MetaTriple(target, verb, noun, negation))

    return triples
