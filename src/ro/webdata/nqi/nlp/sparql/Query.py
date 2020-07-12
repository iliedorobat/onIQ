from ro.webdata.nqi.common.constants import STR_SEPARATOR, VARIABLE_PREFIX
from ro.webdata.nqi.nlp.sentence.constants import TYPE_SELECT_CLAUSE, TYPE_WHERE_CLAUSE
from ro.webdata.nqi.nlp.sparql.MetaTriple import MetaTriple
from ro.webdata.nqi.nlp.sparql.Triple import Triple
from ro.webdata.nqi.rdf import parser
from ro.webdata.nqi.rdf.Match import Match


# TODO: check if the sentence start with WHEN and WHERE
class Query:
    def __init__(self, endpoint, statements):
        self.targets = _get_targets(statements)
        self.meta_triples = _get_meta_triples(endpoint, statements)

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

    def get_where_block(self, indentation='\t'):
        triples_str = ''

        for i in range(len(self.meta_triples)):
            meta_triple = self.meta_triples[i]
            conjunction = meta_triple.conjunction.text.upper() if meta_triple.conjunction is not None else None

            # TODO: OR
            if conjunction is None or conjunction == 'AND':
                triples_str += f'{indentation}' \
                               f'{VARIABLE_PREFIX}{STR_SEPARATOR.join(meta_triple.triple.s)} ' \
                               f'{meta_triple.triple.p} ' \
                               f'{VARIABLE_PREFIX}{meta_triple.triple.o} .'
                triples_str += '\n' if i < len(self.meta_triples) - 1 else ''

        return triples_str

    def get_filter_block(self, indentation='\t'):
        filter_str = ''

        for i in range(len(self.meta_triples)):
            meta_triple = self.meta_triples[i]
            filter_str += f'{indentation}{str(meta_triple.filter_clause)}'
            filter_str += ' .\n' if i < len(self.meta_triples) - 1 else ''

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


def _get_targets(statements):
    targets = []

    for stmt in statements:
        target = _get_target(stmt)

        if target is not None:
            targets.append(target)

    return targets


def _get_target(stmt):
    if stmt.type == TYPE_SELECT_CLAUSE:
        return next((
            token for token in stmt.phrase
            if token.pos_ == "NOUN" and token.tag_ in ["NN", "NNS"]
        ), None)

    return None


def _get_meta_triples(endpoint, statements):
    m_triples: [MetaTriple] = []

    for stmt in statements:
        verb_stmt = stmt.action.verb_stmt
        verb = verb_stmt.main_vb \
            if verb_stmt.main_vb is not None \
            else verb_stmt.aux_vb
        negation = verb_stmt.neg
        conjunction = stmt.conjunction

        prop = _get_matched_property(endpoint, verb)
        print('pp:', prop)
        target = _get_target(stmt)

        triple_s = target.lemma_
        triple_p = prop.prop_name_extended if prop is not None else None
        triple_o = prop.prop_name_extended.replace(':', '_') if prop is not None else None

        new_triple = Triple(triple_s, triple_p, triple_o)

        if stmt.type == TYPE_SELECT_CLAUSE:
            _append_select(stmt, m_triples, prop, target, negation, conjunction)
        elif stmt.type == TYPE_WHERE_CLAUSE:
            # TODO: if len(noun_list) == 0 ???
            noun_list = [token for token in stmt.phrase if token.pos_ == "NOUN"]
            for noun in noun_list:
                m_triples.append(MetaTriple(new_triple, noun.text, negation, conjunction))

    return m_triples


def _append_select(stmt, m_triples, prop, target, negation, conjunction):
    pobj_tokens = [token for token in stmt.phrase if token.dep_ == "pobj"]
    triple_s = target.lemma_
    triple_p = prop.prop_name_extended if prop is not None else None
    triple_o = prop.prop_name_extended.replace(':', '_') if prop is not None else None

    # Find if there already exists a triple with the predicate == triple_p
    crr_m_triple = next((
        m_triple for m_triple in m_triples if m_triple.triple.p == triple_p
    ), None)
    new_triple: Triple = crr_m_triple.triple if crr_m_triple is not None else Triple([triple_s], triple_p, triple_o)

    if len(pobj_tokens) == 0:
        if crr_m_triple is not None:
            crr_m_triple.triple.s.append(triple_s)
            crr_m_triple.value.append(target.text)
            crr_m_triple.def_filter_clause(stmt.type)
        else:
            m_triples.append(MetaTriple(new_triple, [target.text], negation, conjunction, stmt.type))
    else:
        for token in pobj_tokens:
            if crr_m_triple is not None:
                crr_m_triple.triple.s.append(triple_s)
                crr_m_triple.value.append(token.text)
                crr_m_triple.def_filter_clause(stmt.type)
            else:
                m_triples.append(MetaTriple(new_triple, [token.text], negation, conjunction, stmt.type))


def _get_matched_property(endpoint, verb):
    properties = parser.get_properties(endpoint)
    match = Match(endpoint, verb.text)

    # TODO: add support for all properties from "matched" set
    for prop in properties:
        for matched in match.matched:
            if prop.prop_name == matched:
                return prop

    return None
