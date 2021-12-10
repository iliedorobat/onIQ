from functools import reduce

from ro.webdata.oniq.common.constants import COMPARISON_OPERATORS, SEPARATOR

from ro.webdata.oniq.model.sentence.Statement import ConsolidatedStatement
from ro.webdata.oniq.model.sparql.MetaTriple import MetaTriple
from ro.webdata.oniq.model.sparql.Pill import Pill
from ro.webdata.oniq.model.rdf.Match import Match
from ro.webdata.oniq.model.rdf.Property import Property
from ro.webdata.oniq.model.sparql.Target import Target, prepare_target_label
from ro.webdata.oniq.model.sparql.Triple import Triple

from ro.webdata.oniq.nlp.noun_utils import get_noun_list


def prepare_where_meta_triple_list(rdf_props: [Property], cons_stmt: ConsolidatedStatement, target: Target):
    return prepare_where_where_list(rdf_props, cons_stmt, [target.label])


def prepare_when_meta_triple_list(rdf_props: [Property], cons_stmt: ConsolidatedStatement, target: Target):
    # target.label
    return prepare_where_where_list(rdf_props, cons_stmt, ['DATE', 'EVENT', 'TIME', 'wasPresentAt'])


def prepare_where_where_list(rdf_props: [Property], cons_stmt: ConsolidatedStatement, target_labels: [str]):
    meta_triple_list = []
    props = _get_matched_properties(rdf_props, target_labels)
    triple_s_name = 'subject'

    pill_list = _prepare_filterable_pills(cons_stmt, triple_s_name)

    for index, prop in enumerate(props):
        # subject_name = _prepare_subject_name(cons_stmt, index)
        triple = Triple(triple_s_name, prop)
        meta_triple = MetaTriple(triple, pill_list)
        meta_triple_list.append(meta_triple)

    return meta_triple_list


# Pregateste lista de "pills" care vor fi utilizate la filtrare
def _prepare_filterable_pills(cons_stmt, triple_s_name):
    pill_list = []
    noun_list = _get_noun_list(cons_stmt.related_phrases)

    for noun in noun_list:
        word = prepare_target_label(noun)
        pill = Pill(triple_s_name, cons_stmt.action.neg, COMPARISON_OPERATORS.CONTAINS, word)
        pill_list.append(pill)

    return pill_list


# Extrage lista de "nouns" din "related_phrases"
def _get_noun_list(related_phrases):
    noun_list = []

    for related_phrase in related_phrases:
        noun_list += get_noun_list(related_phrase.chunk)

    return list(set(noun_list))


def _get_matched_properties(rdf_props: [Property], words: [str]):
    props = []
    match = Match(rdf_props, words)

    for prop in rdf_props:
        for matched in match.matched:
            if prop.prop_name == matched:
                props.append(prop)

    return props


def _prepare_subject_name(cons_stmt: ConsolidatedStatement, index=0):
    # has_main_verb = cons_stmt.action.verb.main_vb is not None
    #
    # if has_main_verb:
    #     return ''

    return 'subject' + SEPARATOR.STRING + str(index)
