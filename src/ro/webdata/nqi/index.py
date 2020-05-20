import logging
import ro.webdata.nqi.nlp.sparql as sparql
import ro.webdata.nqi.rdf.graph_processor as graph
from langdetect import detect


ENDPOINT = "http://localhost:7200/repositories/eCHM"
# QUERY = 'Display the artefacts hosted in Romania'
# QUERY = 'Where can I find some interesting artefacts'
# QUERY = 'Where the artefacts are?'
# QUERY = 'What are some of the most interesting challenges of natural language processing?'
# QUERY = 'Which are the most visited museums which exposed at least 10 but not more than 20 artifacts'
# TODO: handle comparison operators
# QUERY = 'Which are the most visited museums which exposed >= 10 artifacts'
# TODO: handle the and/or
# QUERY = 'What tools and techniques does the Python programming language provide for such work?'
QUERY = 'Find the student name and the student age where instructor name is "Christian"'
# QUERY = 'Give me the most beautiful museums'
SHOULD_PRINT = True

# https://blog.einstein.ai/how-to-talk-to-your-database/

if detect(QUERY) != "en":
    logging.warning(
        f'\n\tLanguage detected: "{detect(QUERY)}"'
        f'\n\tLanguage required: "en"'
    )

sparql_query = sparql.get_query(ENDPOINT, QUERY, SHOULD_PRINT)

if SHOULD_PRINT:
    print(f'\nsparql_query:\n{sparql_query}')

# rdf_parser.parse_rdf("../../../../files/input/rdf/demo_2.rdf")
# properties = graph.generate_properties_map(ENDPOINT)
# for value in properties:
#     print(value)
