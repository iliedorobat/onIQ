import logging
import ro.webdata.nqi.nlp.sparql as sparql
import ro.webdata.nqi.rdf.graph_processor as graph
import ro.webdata.nqi.nlp.test.queries as queries
from langdetect import detect


ENDPOINT = "http://localhost:7200/repositories/eCHM"
QUERY = queries.QUERY_MUSEUM_2

SHOULD_PRINT = True

if detect(QUERY) != "en":
    logging.warning(
        f'\n\tLanguage detected: "{detect(QUERY)}"'
        f'\n\tLanguage required: "en"'
    )

sparql_query = sparql.get_query(ENDPOINT, QUERY, SHOULD_PRINT)

if SHOULD_PRINT:
    print(f'\nsparql_query:\n{sparql_query}')

# https://blog.einstein.ai/how-to-talk-to-your-database/
# rdf_parser.parse_rdf("../../../../files/input/rdf/demo_2.rdf")
# properties = graph.generate_properties_map(ENDPOINT)
# for value in properties:
#     print(value)
