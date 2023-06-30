from typing import List

from ro.webdata.oniq.sparql.NLQuestion import NLQuestion, ANSWER_TYPE
from ro.webdata.oniq.sparql.NounEntity import NounEntity
from ro.webdata.oniq.sparql.triples.Triple import Triple


class SPARQLQuery:
    @staticmethod
    def get_query(nl_question: NLQuestion, targets: List[NounEntity], triples: List[Triple]):
        output = ""

        if nl_question.answer_type == ANSWER_TYPE.BOOL:
            output = "ASK"
        else:
            str_targets = [_target_to_str(nl_question, target) for target in targets]
            output = f"SELECT DISTINCT {' '.join(str_targets)}"

        str_triples = [f"\t{str(triple)}" for triple in triples]
        output += "\n"
        output += "WHERE {\n"
        output += " .\n".join(str_triples) + "\n"
        output += "}"

        str_ordering_triples = list(
            set([
                f"{str(item.order_by)}"
                for item in triples
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
