import spacy

from spacy import displacy
from ro.webdata.nqi.common.constants import SHOULD_PRINT
from ro.webdata.nqi.common.print_utils import print_statements
from ro.webdata.nqi.nlp.parser import get_statements
from ro.webdata.nqi.nlp.sparql.Query import Query

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5')
# nlp = spacy.load('../../../../lib/en_core_web_md/en_core_web_md-2.2.5')


def get_query(endpoint, nl_query):
    sparql_query_skeleton = """
{prefixes}
SELECT {targets}
WHERE {{
    {where_block}
    {filter_statement}
}}
    """

    statements = get_statements(nl_query)
    query = Query(endpoint, statements)

    sparql_query = sparql_query_skeleton.format(
        prefixes=Query.get_prefixes(endpoint),
        targets=query.get_targets_str(),
        where_block=query.get_where_block(),
        filter_statement=query.get_filter_block()
    )

    # return generated_sparql_query.strip()

    if SHOULD_PRINT:
        print(query)
        print_statements(statements)
        print(sparql_query)

    # nlp_query = nlp(query)
    # displacy.serve(nlp_query, style="dep")

    return sparql_query
