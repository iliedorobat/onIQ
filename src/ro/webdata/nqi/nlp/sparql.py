import re
import spacy
from spacy import displacy

import ro.webdata.nqi.rdf.parser as parser
from ro.webdata.nqi.common.print_utils import print_statements
from ro.webdata.nqi.nlp.statement import get_statements

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5')
# nlp = spacy.load('../../../../lib/en_core_web_md/en_core_web_md-2.2.5')


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

    properties = parser.get_properties(endpoint)
    namespaces = parser.get_namespaces(endpoint)

    subject_var = "?s"

    # filter_statement = prepare_filer_statement(endpoint, query, should_print)
    prefixes = prepare_query_prefixes(namespaces)
    # where_block = prepare_query_where_block(properties, subject_var)

    filter_statement = ""
    where_block = ""

    generated_sparql_query = sparql_query.format(
        filter_statement=filter_statement,
        prefixes=prefixes,
        subject_variables="*",
        where_block=where_block
    )

    # return generated_sparql_query.strip()

    statements = get_statements(query, should_print)
    if should_print:
        print_statements(statements, 'statement')
        print(generated_sparql_query)

    nlp_query = nlp(query)
    # displacy.serve(nlp_query, style="dep")

    return generated_sparql_query


def prepare_query_prefixes(namespaces):
    prefixes = ""

    for i in range(len(namespaces)):
        namespace = namespaces[i]
        left_space = ""
        if i > 0:
            left_space = "\n"
        prefixes += left_space + "PREFIX " + namespace.label + ": <" + namespace.name + ">"

    return prefixes


def prepare_query_where_block(properties, subject_var):
    where_block = ""

    for i in range(len(properties)):
        value = properties[i]
        left_space = ""
        if i > 0:
            left_space = "\n\t"
        where_block += left_space + "OPTIONAL { " \
                       + subject_var + " " \
                       + value["prop_name_extended"] \
                       + " ?" + re.sub(':', '_', value["prop_name_extended"]) \
                       + " } ."

    return where_block


def prepare_filer_statement(endpoint, query, should_print=False):
    filter_statement = ""
    statements = get_statements(query)
    graph_properties = parser.get_properties(endpoint)

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
