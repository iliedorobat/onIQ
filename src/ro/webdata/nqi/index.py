import ro.webdata.nqi.nlp.sparql as sparql
import ro.webdata.nqi.rdf.graph_processor as graph


ENDPOINT = "http://localhost:7200/repositories/eCHM"
QUERY = 'Display the artefacts hosted in Romania'
SHOULD_PRINT = True

# https://blog.einstein.ai/how-to-talk-to-your-database/
sparql_query = sparql.get_query(ENDPOINT, QUERY, SHOULD_PRINT)

if SHOULD_PRINT:
    print(f'\nsparql_query:\n{sparql_query}')

# rdf_parser.parse_rdf("../../../../files/input/rdf/demo_2.rdf")
# properties = graph.generate_properties_map(ENDPOINT)
# for value in properties:
#     print(value)
