from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.model.rdf.Match import Match
from ro.webdata.oniq.model.rdf.Property import Property
from ro.webdata.oniq.model.sentence.Statement import ConsolidatedStatement, Statement
from ro.webdata.oniq.model.sparql.MetaTriple import MetaTriple
from ro.webdata.oniq.model.sparql.Pill import Pill
from ro.webdata.oniq.model.sparql.Target import Target
from ro.webdata.oniq.model.sparql.Triple import Triple

from ro.webdata.oniq.common.constants import COMPARISON_OPERATORS, QUESTION_TYPES
from ro.webdata.oniq.common import rdf_utils
from ro.webdata.oniq.nlp.meta_triple import prepare_where_meta_triple
from ro.webdata.oniq.nlp.meta_triples.where_when import prepare_where_meta_triple_list, prepare_when_meta_triple_list
from ro.webdata.oniq.nlp.nlp_utils import is_wh_noun_chunk
from ro.webdata.oniq.nlp.noun_utils import get_nouns
from ro.webdata.oniq.nlp.stmt_utils import consolidate_statement_list
from ro.webdata.oniq.nlp.targets import prepare_target_list


class Query:
    def __init__(self, endpoint: str, statements: [Statement]):
        cons_statements = consolidate_statement_list(statements)
        rdf_props = rdf_utils.get_properties(endpoint)

        self.target_list = _prepare_target_list(rdf_props, cons_statements)
        self.meta_triple_list = _prepare_meta_triple_list(rdf_props, cons_statements)

        echo.target_list(self.target_list)


def _prepare_target_list(rdf_props: [Property], cons_statements: [ConsolidatedStatement]):
    """
    Get the list of unique targets in each statement

    :param rdf_props: TODO
    :param cons_statements: The list of statements
    :return: The list of unique targets
    """

    target_list = []

    for cons_stmt in cons_statements:
        target_list += prepare_target_list(rdf_props, cons_stmt)

    return list(set(target_list))


def _prepare_meta_triple_list(rdf_props: [Property], cons_statements: [Statement]):
    meta_triple_list = []

    for cons_stmt in cons_statements:
        meta_triple = None
        chunk = cons_stmt.phrase.chunk

        if is_wh_noun_chunk(chunk):
            target_list = prepare_target_list(rdf_props, cons_stmt)

            for target in target_list:
                if chunk[0].lower_ == QUESTION_TYPES.WHERE:
                    mt_list = prepare_where_meta_triple_list(rdf_props, cons_stmt, target)
                    print(mt_list)
                elif chunk[0].lower_ == QUESTION_TYPES.WHEN:
                    mt_list = prepare_when_meta_triple_list(rdf_props, cons_stmt, target)
                    print(mt_list)
        else:
            print(chunk)

    return meta_triple_list


def _prepare_meta_triple_list_bk(endpoint: str, statements: [Statement]):
    """
    Generate the list of meta triples

    :param endpoint: The SPARQL endpoint
    :param statements: The list of generated statements
    :return: The list of meta triples
    """

    meta_triple_list = []

    for stmt in statements:
        meta_triple = None
        first_word = stmt.phrase[0]
        backend_prop = _get_backend_property(endpoint, stmt.action.verb)

        # TODO: 'when'
        if first_word.lower_ in ['where']:
            meta_triple = prepare_where_meta_triple(stmt.related_phrases, backend_prop)
        else:
            for noun in get_nouns([stmt.phrase]):
                target = Target(noun)
                meta_triple = _prepare_meta_triple(backend_prop, target, stmt)

        if meta_triple is not None:
            meta_triple_list.append(meta_triple)

    return meta_triple_list


def _prepare_meta_triple(prop: Property, target: Target, stmt: Statement):
    pill_list = []
    triple = Triple(target, prop)

    for value in get_nouns(stmt.related_phrases):
        # TODO: triple.s is not correct !!!
        pill = Pill(triple.s, stmt.action.neg, COMPARISON_OPERATORS.CONTAINS, value)
        pill_list.append(pill)

    meta_triple = MetaTriple(triple, pill_list)

    return meta_triple


def _get_backend_property(endpoint, primary_verb):
    """
    TODO
    Get the name of the backend property which best matches main_verb.
    # Get nothing (None) if main_verb is missing.

    :param endpoint: The SPARQL endpoint
    :param verb: The verb statement
    :return: The name of the backend property
    """

    # # if the main verb is missing
    # if not verb.has_main_verb():
    #     return None
    # # TODO: momentan trateaza exemplul urmator: "Where is the museum?"
    # primary_verb = verb.main_vb.lemma_ if verb.main_vb is not None else verb.aux_vbs[0].lemma_
    # primary_verb = 'location' if primary_verb == 'be' else primary_verb

    properties = rdf_utils.get_properties(endpoint)
    match = Match(endpoint, [primary_verb])

    # TODO: add support for all properties from "matched" set
    for prop in properties:
        for matched in match.matched:
            if prop.prop_name == matched:
                return prop

    return None
