import spacy
from spacy import displacy

from ro.webdata.oniq.model.sparql.Query import Query
from ro.webdata.oniq.nlp.statements import consolidate_statement_list, get_statement_list


nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5')
# nlp = spacy.load('../../../../lib/en_core_web_md/en_core_web_md-2.2.5')


_QUERY_SKELETON = "{prefixes}" \
                  "SELECT {targets}" \
                  "WHERE {{" \
                  "{where_block}" \
                  "{filter_statement}" \
                  "}}"


class MetaQuery:
    # nl_query: The query provided by the user in natural language
    def __init__(self, endpoint, question):
        # TODO: nlp("document", disable=["parser"])
        document = nlp(question)
        statements = get_statement_list(document)
        query = Query(endpoint, statements)
        #
        # TODO: query.get_str method
        # self.query = _QUERY_SKELETON.format(
        #     prefixes=Query.get_prefixes(endpoint),
        #     targets=query.get_targets_str(),
        #     where_block=query.get_where_block(),
        #     filter_statement=query.get_filter_block()
        # )

        # nlp_query = nlp(nl_query)
        # displacy.serve(nlp_query, style="dep")
