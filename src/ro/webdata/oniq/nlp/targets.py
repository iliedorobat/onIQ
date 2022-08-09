from ro.webdata.oniq.model.rdf.Match import Match
from ro.webdata.oniq.model.rdf.Property import Property
from ro.webdata.oniq.model.sentence.Statement import ConsolidatedStatement
from ro.webdata.oniq.model.sparql.Target import Target, prepare_target_label

from ro.webdata.oniq.nlp.noun_utils import get_noun_list


def prepare_target_list(rdf_props: [Property], cons_stmt: ConsolidatedStatement):
    """
    Get the list of unique targets for the input statement

    :param rdf_props: TODO: doc
    :param cons_stmt: The input statement
    :return: The list of unique targets
    """

    target_list = []
    noun_list = get_noun_list(cons_stmt.phrase.chunk)

    for noun in noun_list:
        if cons_stmt.phrase.question_type is not None:
            target_label = prepare_target_label(noun)
            match = Match(rdf_props, [target_label])

            # TODO: complete the list with 'when' etc.
            if target_label in ['where']:
                for prop in rdf_props:
                    for matched in match.matched:
                        if prop.prop_name == matched:
                            target = Target(noun, prop)
                            if target not in target_list:
                                target_list.append(target)
            else:
                target = Target(noun, None)
                if target not in target_list:
                    target_list.append(target)

    return target_list
