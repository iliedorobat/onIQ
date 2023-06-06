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
            output = "SELECT DISTINCT"
            for target in self.targets:
                output += f" {target.to_var()}"

        output += "\nWHERE {"
        for triple in self.triples:
            output += f"\n\t{str(triple)} ."
        output += "\n}"

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
            output += "target_nouns = [\n"
            for target in self.targets:
                output += f"\t{target.to_var()}\n"
            output += "]\n"

        output += "raw_triples = [\n"
        for raw_triple in self.raw_triples:
            output += f"\t<{str(raw_triple)}>\n"
        output += "]"

        return output


def _get_query_type(nl_question):
    if nl_question.main_type == QUESTION_TYPES.AUX_ASK:
        return QUERY_TYPES.ASK
    elif nl_question.main_type == QUESTION_TYPES.HOW:
        return QUERY_TYPES.COUNT

    return QUERY_TYPES.SELECT
