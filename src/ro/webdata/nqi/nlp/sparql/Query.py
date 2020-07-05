from ro.webdata.nqi.nlp.sentence.constants import TYPE_SELECT_CLAUSE, TYPE_WHERE_CLAUSE


class Query:
    def __init__(self, statements):
        self.targets = _get_targets(statements)
        self.meta_triples = _get_meta_triples(statements, self.targets)

    def get_targets_str(self):
        targets_str = ''

        for i in range(len(self.targets)):
            targets_str += f'?{self.targets[i]}'
            targets_str += ' ' if i < len(self.targets) - 1 else ''

        return targets_str

    def get_triples_str(self):
        triples_str = ''

        for i in range(len(self.meta_triples)):
            meta_triple = self.meta_triples[i]
            conjunction = meta_triple.conjunction.text.upper() if meta_triple.conjunction is not None else None

            # TODO: OR
            if conjunction is None or conjunction == 'AND':
                if conjunction == 'AND':
                    triples_str += ' .\n'

                # TODO: predicate
                triples_str += f'?{meta_triple.triple.s} {meta_triple.triple.p} ?{meta_triple.triple.o}'

        return triples_str

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
    def __init__(self, s=None, p=None, o=None, negation=None, conjunction=None):
        self.triple = Triple(s, p, o)
        self.negation = negation
        self.conjunction = conjunction

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}meta triple: {{\n'
            f'{indentation}\ttriple: {Triple.get_str(self.triple)},\n'
            f'{indentation}\tnegation: {self.negation}\n'
            f'{indentation}\tconjunction: {self.conjunction}\n'
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
                if token.pos_ == "NOUN" and token.tag_ in ["NN", "NNS"]
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
            conjunction = stmt.conjunction
            noun_list = [token for token in stmt.phrase if token.pos_ == "NOUN"]

            for target in targets:
                for noun in noun_list:
                    triples.append(MetaTriple(target, verb, noun, negation, conjunction))

    return triples
