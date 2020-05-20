import spacy

import ro.webdata.nqi.rdf.graph_processor as graph
from ro.webdata.nqi.common.print_utils import print_statements
from ro.webdata.nqi.nlp.statement import get_statements

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5')


# TODO:
def get_query(endpoint, query, should_print=False):
    sparql_query = """
{prefixes}
SELECT {subject_variables}
WHERE {{
    {where_block}
    {filter_statement}
}}
    """

    properties = graph.generate_properties_map(endpoint)
    namespaces = graph.generate_namespaces_map(properties)

    subject_var = "?s"

    # filter_statement = prepare_filer_statement(endpoint, query, should_print)
    # prefixes = prepare_query_prefixes(namespaces)
    # where_block = prepare_query_where_block(properties, subject_var)
    #
    # generated_sparql_query = sparql_query.format(
    #     filter_statement=filter_statement,
    #     prefixes=prefixes,
    #     subject_variables="*",
    #     where_block=where_block
    # )
    #
    # return generated_sparql_query.strip()

    statements = get_statements(query, should_print)
    print_statements(statements)

    return ""


def prepare_query_prefixes(namespaces):
    prefixes = ""

    for i in range(len(namespaces)):
        namespace = namespaces[i]
        left_space = ""
        if i > 0:
            left_space = "\n"
        prefixes += left_space + "PREFIX " + namespace["ns_label"] + ": <" + namespace["ns_name"] + ">"

    return prefixes


def prepare_query_where_block(properties, subject_var):
    where_block = ""

    for i in range(len(properties)):
        value = properties[i]
        left_space = ""
        if i > 0:
            left_space = "\n\t"
        where_block += left_space + "OPTIONAL { " + subject_var + " " + value["short_name"] + " ?" + value[
            "prop_name_extended"] + " } ."

    return where_block


def prepare_filer_statement(endpoint, query, should_print=False):
    filter_statement = ""
    statements = get_statements(query)
    graph_properties = graph.generate_properties_map(endpoint)

    for i in range(len(statements)):
        statement = statements[i]

        if should_print:
            print(f'statement[{i}]: {statement}')

        if i == 0:
            filter_statement = "FILTER ("

        if statement["is_main_statement"]:
            # TODO:
            # filter_statement += "\n\t\t" + "contains(" + subject_var + ", \"" + str(stmt["complement"][0]) + "\") ."
            None
        else:
            for g_property in graph_properties:
                for complement in statement["complement"]:
                    # TODO: nlp validation (use the lemmatization to find similar words)
                    if g_property["prop_label"] == complement:
                        filter_statement += "\n\t\t" + "contains(" + g_property["short_name"] + ", \"" + str(
                            statement["predicate"]) + "\") ."

        if i == len(statements) - 1:
            filter_statement += "\n\t)"

    return filter_statement


def test_statements():
    print()
    get_statements('which is the largest city in the world?')
    # TODO:
    get_statements('Show me the most interesting, visited and the most beautiful museums')
    # TODO: but unlisted...
    get_statements('which are the first 10 artifacts hosted by John Kane but unlisted')
    get_statements('tell me where the TX\'s location is')
    get_statements('where the TX\'s location is')
    get_statements('which is the most interesting museum?')
    get_statements('give me the artifacts hosted by somebody')
    get_statements('Show me the most interesting museums in New York')
    get_statements('How many players from the United States play PG')

