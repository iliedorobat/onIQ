from ro.webdata.oniq.common.constants import APP_MODE
from ro.webdata.oniq.model.sparql.MetaQuery import MetaQuery
from ro.webdata.oniq.test.dataset import pairs

ENDPOINT = "http://localhost:7200/repositories/TESTING_BCU_CLUJ"
ENDPOINT = "http://localhost:7200/repositories/eCHO"

QUERY = 'Which paintings are not located in Bacau?'
if APP_MODE.IS_TEST_MODE is False:
    sparql_query = MetaQuery(ENDPOINT, QUERY)
else:
    for pair in pairs:
        sparql_query = MetaQuery(ENDPOINT, pair["query"])


# # https://blog.einstein.ai/how-to-talk-to-your-database/
# rdf_utils.parse_rdf("../../../../files/input/rdf/demo_2.rdf")


# from ro.webdata.nqi.rdf.Match import Match
# from ro.webdata.nqi.rdf import rdf_utils
# match = Match(ENDPOINT, 'location')
# print('location:', match)


