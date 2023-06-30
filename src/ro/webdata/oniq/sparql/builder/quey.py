from typing import List

from ro.webdata.oniq.sparql.NLQuestion import NLQuestion, ANSWER_TYPE
from ro.webdata.oniq.sparql.NounEntity import NounEntity
from ro.webdata.oniq.sparql.filters.Filters import Filters
from ro.webdata.oniq.sparql.targets.Targets import Targets
from ro.webdata.oniq.sparql.triples.Triple import Triple
from ro.webdata.oniq.sparql.triples.Triples import Triples


class SPARQLQuery:
    @staticmethod
    def get_query(nl_question: NLQuestion, targets: Targets, triples: Triples, filters: Filters):
        target_list: List[NounEntity] = targets.values
        triple_list: List[Triple] = triples.values
        filter_list: List[str] = filters.values

        output = ""

        if nl_question.answer_type == ANSWER_TYPE.BOOL:
            output = "ASK"
        else:
            str_targets = [_target_to_str(nl_question, target) for target in target_list]
            output = f"SELECT DISTINCT {' '.join(str_targets)}"

        str_triples = [f"\t{str(triple)}" for triple in triple_list]
        str_filters = [f"\t{str(f)}" for f in filter_list]
        str_where = str_triples + str_filters

        output += "\n"
        output += "WHERE {\n"
        output += " .\n".join(str_where) + "\n"
        output += "}"

        str_ordering_triples = list(
            set([
                f"{str(item.order_by)}"
                for item in triple_list
                if item.is_ordering_triple()
            ])
        )

        if len(str_ordering_triples) > 0:
            output += "\n"
            output += f"ORDER BY {' '.join(str_ordering_triples)}"

        return output


def _target_to_str(nl_question, target: NounEntity):
    if nl_question.answer_type == ANSWER_TYPE.NUMBER:
        return f"COUNT({target.to_var()})"
    return target.to_var()
