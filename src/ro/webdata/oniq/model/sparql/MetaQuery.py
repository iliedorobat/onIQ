import warnings

import spacy

from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.nlp.stmt_utils import get_statement_list

nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en_core_web_md')


_QUERY_SKELETON = "{prefixes}" \
                  "SELECT {targets}" \
                  "WHERE {{" \
                  "{where_block}" \
                  "{filter_statement}" \
                  "}}"


class MetaQuery:
    # nl_query: The query provided by the user in natural language

    warnings.warn("deprecated in favour of SPARQLQuery", DeprecationWarning)

    def __init__(self, endpoint, question):
        # TODO: nlp("document", disable=["parser"])
        document = nlp(question)
        statements = get_statement_list(document)
        # query = Query(endpoint, statements)
        #
        # TODO: query.get_str method
        # self.query = _QUERY_SKELETON.format(
        #     prefixes=Query.get_prefixes(endpoint),
        #     targets=query.get_targets_str(),
        #     where_block=query.get_where_block(),
        #     filter_statement=query.get_filter_block()
        # )

        # nlp_query = nlp(question)
        # displacy.serve(nlp_query, style="dep", port=7700)
