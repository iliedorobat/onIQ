import ro.webdata.nqi.nlp.sparql.sparql as sparql

from ro.webdata.nqi.common.print_utils import print_lang_warning

ENDPOINT = "http://localhost:7200/repositories/TESTING_BCU_CLUJ"
ENDPOINT = "http://localhost:7200/repositories/eCHO"

QUERY = 'Which paintings are located in Bacau?'
QUERY = 'Which paintings and statues are located in Bacau?'
print_lang_warning(QUERY)
sparql_query = sparql.get_query(ENDPOINT, QUERY)


# # https://blog.einstein.ai/how-to-talk-to-your-database/
# parser.parse_rdf("../../../../files/input/rdf/demo_2.rdf")


# from ro.webdata.nqi.rdf.Match import Match
# from ro.webdata.nqi.rdf import parser
# match = Match(ENDPOINT, 'location')
# print('location:', match)


