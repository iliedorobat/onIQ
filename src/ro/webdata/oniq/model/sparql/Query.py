from functools import reduce

from spacy.tokens import Span

from ro.webdata.oniq.model.rdf.Match import Match
from ro.webdata.oniq.model.rdf.Property import Property
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.model.sentence.Verb import Verb
from ro.webdata.oniq.model.sparql.MetaTriple import MetaTriple
from ro.webdata.oniq.model.sparql.Pill import Pill, Pills
from ro.webdata.oniq.model.sparql.Target import Target
from ro.webdata.oniq.model.sparql.Triple import Triple

from ro.webdata.oniq.common.constants import COMPARISON_OPERATORS, SEPARATOR, PRINT_MODE
from ro.webdata.oniq.common import rdf_utils
from ro.webdata.oniq.nlp.meta_triple import prepare_where_meta_triple
from ro.webdata.oniq.nlp.phrase import get_nouns


class Query:
    def __init__(self, endpoint: str, statements: [Statement]):
        self.target_list = _prepare_target_list(statements)
        # self.meta_triple_list = _prepare_meta_triple_list(endpoint, statements)

        for target in self.target_list:
            if PRINT_MODE.PRINT_TARGET is True:
                print(target)


    @staticmethod
    def get_prefixes(endpoint):
        namespaces = rdf_utils.get_namespaces(endpoint)
        prefixes = ''

        for i in range(len(namespaces)):
            namespace = namespaces[i]
            left_space = '\n' if i > 0 else ''
            prefixes += f'{left_space}PREFIX {namespace.label}: <{namespace.name}>'

        return prefixes

    def get_targets_str(self, indentation=''):
        targets_str = ''

        for target in self.targets:
            targets_str += target.get_variable_pattern()

        return targets_str.rstrip()

    def get_where_block(self, indentation='\t'):
        triples_str = ''

        for meta_triple in self.meta_triples:
            triples_str += meta_triple.triple.get_triple_pattern() + '.\n'

        return triples_str.rstrip()

    def get_filter_block(self, indentation='\t'):
        filter_str = ''

        for meta_triple in self.meta_triples:
            filter_str += f'{meta_triple.filter.get_filter_pattern()}\n'

        return filter_str.rstrip()

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


def _prepare_targets(endpoint, statements):
    targets = []
    prev_prop = None
    prev_stmt_type = None

    for i in range(0, len(statements)):
        stmt = statements[i]
        verb = stmt.action.verb.get_verb()
        prop = _get_matched_property(endpoint, verb)
        target_token = _get_target_token(stmt)

        if target_token is not None:
            if stmt.type != prev_stmt_type or not prop.__eq__(prev_prop):
                # TODO: 'Which statues do not have more than three owners?'
                targets.append(Target(target_token.lemma_, [target_token], stmt.type))
            else:
                target = targets[i - 1]
                target.values.append(target_token)
                target.name = SEPARATOR.STRING.join([value.lemma_ for value in target.values])

            prev_prop = prop
            prev_stmt_type = stmt.type

    return targets


def _get_target_token(stmt):
    """
    Get the target from the user query (the noun in the TYPE_SELECT_CLAUSE statement)
    :param stmt: The query statement
    :return: The noun (singular / mass / plural)
    """

    if stmt.type == SENTENCE_TYPE.SELECT_CLAUSE:
        return next((
            token for token in stmt.phrase
            if token.pos_ == "NOUN" and token.tag_ in ["NN", "NNS"]
        ), None)

    return None


"""
_consolidate_meta_triples documentation
input = Which paintings or statues are located in Bacau?

prep_meta_triples = [
    {
        triple: { <painting_statue> <edm:currentLocation> <edm_currentLocation> },
        pill: target pills: [ { [] <painting_statue> <contains> <paintings> } ]
    },
    {
        triple: { <painting_statue> <edm:currentLocation> <edm_currentLocation> },
        pill: target pills: [ { [or] <painting_statue> <contains> <statues> } ]
    }
]
meta_triples = [
    {
        triple: { <painting_statue> <edm:currentLocation> <edm_currentLocation> },
        pill: target pills: [
            { [] <painting_statue> <contains> <paintings> },
            { [or] <painting_statue> <contains> <statues> }
        ]
    }
]
"""


def _consolidate_meta_triples(endpoint, statements):
    prep_meta_triples: [MetaTriple] = _prepare_meta_triples(endpoint, statements)
    meta_triples = _get_base_meta_triples(endpoint, statements)

    for prep_meta_triple in prep_meta_triples:
        for meta_triple in meta_triples:
            if meta_triple.triple.__eq__(prep_meta_triple.triple):
                meta_triple.pills.targets = meta_triple.pills.targets + prep_meta_triple.pills.targets

    print('------')
    for meta in prep_meta_triples:
        print(meta)
    print('------')
    for meta in meta_triples:
        print(meta)

    return meta_triples


"""
_get_base_meta_triples documentation
input = Which paintings or statues are located in Bacau?

in_meta_triples = [
    {
        triple: { <painting_statue> <edm:currentLocation> <edm_currentLocation> },
        pill: target pills: [{  <painting_statue> <contains> <paintings> }]
    },
    {
        triple: { <painting_statue> <edm:currentLocation> <edm_currentLocation> },
        pill: target pills: [{ [or] <painting_statue> <contains> <statues> }]
    }
]
base_meta_triples = [
    {
        triple: { <painting_statue> <edm:currentLocation> <edm_currentLocation> },
        pill: None
    }
]
"""


def _get_base_meta_triples(endpoint, statements):
    base_meta_triples: [MetaTriple] = []
    in_meta_triples: [MetaTriple] = _prepare_meta_triples(endpoint, statements)

    for in_meta_triple in in_meta_triples:
        in_triple = in_meta_triple.triple

        filtered = [meta_triple.triple for meta_triple in base_meta_triples if in_triple.__eq__(meta_triple.triple)]
        if len(filtered) == 0:
            base_meta_triples.append(MetaTriple(in_triple))

    return base_meta_triples


def _prepare_meta_triples(endpoint, statements):
    meta_triples: [MetaTriple] = []
    targets = _prepare_targets(endpoint, statements)

    for stmt in statements:
        verb = stmt.action.verb.get_verb()
        negation = stmt.action.verb.neg
        logical_operation = stmt.logical_operation

        prop = _get_matched_property(endpoint, verb)
        target_item = _get_target_token(stmt)

        if stmt.type == SENTENCE_TYPE.SELECT_CLAUSE:
            target = list(filter(lambda item: target_item in item.values != -1, targets))
            triple_s = target[0].name
            triple_p = prop.prop_name_extended if prop is not None else None
            triple_o = prop.prop_name_extended.replace(SEPARATOR.NAMESPACE, SEPARATOR.STRING) if prop is not None else None

            triple = Triple(triple_s, triple_p, triple_o)
            target_pill = Pill(logical_operation, triple_s, negation, COMPARISON_OPERATORS.CONTAINS, target_item.text)
            pills = Pills([target_pill])

            meta_triples.append(MetaTriple(triple, pills))
        elif stmt.type == SENTENCE_TYPE.WHERE_CLAUSE:
            # TODO: TYPE_WHERE_CLAUSE
            print(f'Query.py: stmt.type {stmt.type} is not implemented')

    return meta_triples


def _get_matched_property(endpoint, verb):
    # if there is an auxiliary verb
    if isinstance(verb, list):
        return None

    properties = rdf_utils.get_properties(endpoint)
    match = Match(endpoint, verb.text)

    # TODO: add support for all properties from "matched" set
    for prop in properties:
        for matched in match.matched:
            if prop.prop_name == matched:
                return prop

    return None
