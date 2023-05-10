from test.ro.webdata.test.oniq.endpoint.common.test_CSVService import TestCSVService
from test.ro.webdata.test.oniq.endpoint.common.translator.test_CSVTranslator import TestCSVTranslator, TestCSVBasicTranslator
from test.ro.webdata.test.oniq.endpoint.common.translator.test_URITranslator import TestURITranslator
from test.ro.webdata.test.oniq.endpoint.dbpedia.test_lookup import TestLookupService
from test.ro.webdata.test.oniq.endpoint.dbpedia.test_query import TestDBpediaQueryService

# common pkg tests
TestURITranslator.run()
TestCSVTranslator.run()
TestCSVBasicTranslator.run()
TestCSVService.run()

# dbpedia pkg tests
TestDBpediaQueryService.run()

# lookup pkg tests
TestLookupService.run()
