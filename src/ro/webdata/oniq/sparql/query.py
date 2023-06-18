from typing import List

from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, QUESTION_TYPES
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.final_triples.Triple import Triple
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class QUERY_TYPES:
    ASK = "ASK"
    COUNT = "COUNT"
    SELECT = "SELECT"


class SPARQLQuery:
    def __init__(self, nl_question: NLQuestion, targets: List[NounEntity], triples: List[Triple]):
        self.nl_question = nl_question
        self.targets = targets
        self.triples = triples
        self.query_type = _get_query_type(self.nl_question)

    def generate_query(self):
        output = ""

        if self.query_type == QUERY_TYPES.ASK:
            output = "ASK"
        else:
            str_targets = [target.to_var() for target in self.targets]
            output = f"SELECT DISTINCT {' '.join(str_targets)}"

        str_triples = [f"\t{str(triple)}" for triple in self.triples]
        output += "\n"
        output += "WHERE {\n"
        output += " .\n".join(str_triples) + "\n"
        output += "}"

        str_ordering_triples = list(
            set([
                f"{str(item.order_by)}"
                for item in self.triples
                if item.is_ordering_triple()
            ])
        )

        if len(str_ordering_triples) > 0:
            output += "\n"
            output += f"ORDER BY {' '.join(str_ordering_triples)}"

        return output


class SPARQLRawQuery:
    def __init__(self, nl_question: NLQuestion, targets: List[NounEntity], raw_triples: List[RawTriple]):
        self.nl_question = nl_question
        self.targets = targets
        self.raw_triples = raw_triples
        self.query_type = _get_query_type(self.nl_question)

    def generate_query(self):
        output = f'query_type = {self.query_type}\n'

        if self.query_type == QUERY_TYPES.ASK:
            output += "target_nouns = []\n"
        else:
            str_targets = [f"\t{target.to_var()}" for target in self.targets]
            output += "target_nouns = [\n"
            output += '\n'.join(str_targets) + "\n"
            output += "]\n"

        str_triples = [f"\t<{str(raw_triple)}>" for raw_triple in self.raw_triples]
        output += "raw_triples = [\n"
        output += "\n".join(str_triples) + "\n"
        output += "]"

        str_ordering_triples = list(
            # E.g.: "Which musician wrote the most books?"
            set([
                f"\t{str(item.order_by)}\n"
                for item in self.raw_triples
                if item.is_ordering_triple()
            ])
        )

        if len(str_ordering_triples) > 0:
            output += "\n"
            output += f"order_by = [\n"
            output += "".join(str_ordering_triples)
            output += "]"

        return output


def _get_query_type(nl_question):
    if nl_question.main_type == QUESTION_TYPES.AUX_ASK:
        return QUERY_TYPES.ASK
    elif nl_question.main_type == QUESTION_TYPES.HOW_COUNT:
        return QUERY_TYPES.COUNT

    return QUERY_TYPES.SELECT
