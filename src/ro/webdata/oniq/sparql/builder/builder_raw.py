from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.sparql.NLQuestion import NLQuestion
from ro.webdata.oniq.sparql.triples.raw_triples.RawTriples import RawTriples


class SPARQLRawBuilder:
    def __init__(self, endpoint, input_question, print_deps):
        self.nl_question = NLQuestion(input_question)
        self.raw_triples = RawTriples(self.nl_question)

        if print_deps:
            echo.deps_list(self.nl_question.question)

    def to_sparql_query(self):
        raw_query = ""

        str_triples = [f"\t<{str(raw_triple)}>" for raw_triple in self.raw_triples.values]
        raw_query += "raw_triples = [\n"
        raw_query += "\n".join(str_triples) + "\n"
        raw_query += "]"

        return raw_query
