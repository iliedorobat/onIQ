from functools import reduce


from ro.webdata.oniq.model.sparql.MetaTriple import MetaTriple
from ro.webdata.oniq.model.sparql.Pill import Pill
from ro.webdata.oniq.model.sparql.Triple import Triple

from ro.webdata.oniq.common.constants import COMPARISON_OPERATORS, SEPARATOR
from ro.webdata.oniq.nlp.noun_utils import get_nouns


# e.g.: 'Where is the museum?'
# e.g.: 'Where are the coins and swords located?'
# DEPRECATED
def prepare_where_meta_triple(related_phrases, backend_prop):
    noun_list = get_nouns(related_phrases)
    target = reduce(
        (lambda x, y: x.lower_ + SEPARATOR.STRING + y.lower_),
        noun_list
    )
    triple = Triple(target, backend_prop)

    pill_list = [
        Pill(target, None, COMPARISON_OPERATORS.CONTAINS, noun.lemma_)
        for noun in noun_list
    ]

    return MetaTriple(triple, pill_list)
