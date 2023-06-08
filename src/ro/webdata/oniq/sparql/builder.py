from typing import List

from ro.webdata.oniq.sparql.builder_raw import SPARQLRawBuilder
from ro.webdata.oniq.sparql.model.final_triples.Triple import Triple
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.query import SPARQLQuery


class SPARQLBuilder:
    def __init__(self, endpoint, input_question, print_deps):
        raw_builder = SPARQLRawBuilder(endpoint, input_question, print_deps)

        self.nl_question = raw_builder.nl_question
        self.targets = raw_builder.targets
        self.triples = _init_triples(raw_builder.main_triples, raw_builder.main_triples, False)
        self.order_by_items = _init_triples(raw_builder.main_triples, raw_builder.order_by_triples, True)

        print()

    def to_sparql_query(self):
        query = SPARQLQuery(self.nl_question, self.targets, self.triples)
        return query.generate_query()


def _init_triples(base_raw_triples: List[RawTriple], raw_triples: List[RawTriple], is_ordering: bool):
    triples = []

    for raw_triple in raw_triples:
        triple = Triple(base_raw_triples, raw_triple, is_ordering)
        triples.append(triple)

    return triples


def _get_entities(question: str):
    entities_uri = f'http://localhost:8200/{PATHS.ENTITIES}?{ACCESSORS.QUESTION}={question}'
    entities_response = requests.get(entities_uri)
    return json.loads(entities_response.content)
