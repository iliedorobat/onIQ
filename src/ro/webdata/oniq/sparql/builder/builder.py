import json

import requests

from ro.webdata.oniq.service.query_const import ACCESSORS, PATHS
from ro.webdata.oniq.sparql.builder.builder_raw import SPARQLRawBuilder
from ro.webdata.oniq.sparql.builder.builder_raw_utils import get_improved_raw_triples
from ro.webdata.oniq.sparql.builder.quey import SPARQLQuery
from ro.webdata.oniq.sparql.filters.Filters import Filters
from ro.webdata.oniq.sparql.targets.Targets import Targets
from ro.webdata.oniq.sparql.triples.Triples import Triples
from ro.webdata.oniq.sparql.triples.raw_triples.OrderByRawTriple import OrderByRawTriple
from ro.webdata.oniq.sparql.triples.raw_triples.generator.RDFTypeRawTriple import RDFTypeRawTriple


class SPARQLBuilder:
    def __init__(self, endpoint, input_question, print_deps):
        raw_builder = SPARQLRawBuilder(endpoint, input_question, print_deps)
        raw_triples_values = _prepare_raw_triples(raw_builder)
        raw_triples_values = get_improved_raw_triples(raw_triples_values, raw_builder.nl_question)

        triples = Triples(raw_triples_values)

        self.nl_question = raw_builder.nl_question
        self.targets = Targets(self.nl_question, triples.values)
        self.triples = triples
        self.filters = Filters(triples.values)

    def to_sparql_query(self):
        return SPARQLQuery.get_query(
            self.nl_question,
            self.targets,
            self.triples,
            self.filters
        )


def _prepare_raw_triples(raw_builder: SPARQLRawBuilder):
    rdf_types = RDFTypeRawTriple.generate_rdf_types(
        raw_builder.nl_question.question,
        raw_builder.raw_triples.values
    )
    raw_triples = raw_builder.raw_triples.values + rdf_types

    order_by_triples = OrderByRawTriple.prepare_extra_raw_triples(
        raw_builder.nl_question,
        raw_builder.raw_triples.values
    )
    # Exclude the triples used in the ORDER BY statement.
    # Using "set" will change the order or elements.
    # E.g.: "Which museum in New York has the most visitors?"
    main_triples = [
        raw_triple for raw_triple in raw_triples
        if raw_triple not in order_by_triples
    ]

    return main_triples + order_by_triples


def _get_entities(question: str):
    entities_uri = f'http://localhost:8200/{PATHS.ENTITIES}?{ACCESSORS.QUESTION}={question}'
    entities_response = requests.get(entities_uri)
    return json.loads(entities_response.content)
