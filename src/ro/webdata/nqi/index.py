import ro.webdata.nqi.nlp.sparql as sparql
import ro.webdata.nqi.rdf.parser as parser

from ro.webdata.nqi.common.constants import SHOULD_PRINT
from ro.webdata.nqi.common.print_utils import print_lang_warning
from ro.webdata.nqi.rdf.Match import Match

ENDPOINT = "http://localhost:7200/repositories/TESTING_BCU_CLUJ"
QUERY = 'when the artifact was issued?'
QUERY = 'when the artifacts was published?'

print_lang_warning(QUERY)
sparql_query = sparql.get_query(ENDPOINT, QUERY, SHOULD_PRINT)


# # https://blog.einstein.ai/how-to-talk-to-your-database/
# parser.parse_rdf("../../../../files/input/rdf/demo_2.rdf")
properties = parser.get_properties(ENDPOINT)
match = Match('published', properties)
print(match)
