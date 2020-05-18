import spacy
from iteration_utilities import unique_everseen
from spacy import displacy

import ro.webdata.nqi.rdf.graph_processor as graph
from ro.webdata.nqi.common.constants import NAMED_ENTITY_MAP
from ro.webdata.nqi.common.nlp_utils import get_wh_words, retokenize
from ro.webdata.nqi.common.print_utils import print_tokens

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5')


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

    filter_statement = prepare_filer_statement(endpoint, query, should_print)
    prefixes = prepare_query_prefixes(namespaces)
    where_block = prepare_query_where_block(properties, subject_var)

    generated_sparql_query = sparql_query.format(
        filter_statement=filter_statement,
        prefixes=prefixes,
        subject_variables="*",
        where_block=where_block
    )

    return generated_sparql_query.strip()


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
    statements = statements_generator(query)
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


def statements_generator(query, should_print=False):
    nlp("document", disable=["parser"])
    document = nlp(query)

    if should_print:
        print(f'query: {document}')

    statements = []
    sentences = document.sents
    for sentence in sentences:
        WH_WORDS = get_wh_words(sentence)
        retokenize(document, sentence)

        if should_print:
            print_tokens(document)
        displacy.serve(document, style="dep")
        # displacy.serve(document, style="ent")

        for chunk in document.noun_chunks:
            statement = {}
            print("chunk:", chunk)
            if chunk.root.tag_[0: 2] == "NN":
                head = None

                # TODO: recursive head.head.head...
                if chunk.root.head.tag_[0: 2] == "VB":
                    head = chunk.root.head
                    statement["is_main_statement"] = True
                elif chunk.root.head.head.tag_[0: 2] == "VB":
                    head = chunk.root.head.head
                    statement["is_main_statement"] = False
                else:
                    statement["is_main_statement"] = False

                statement["verb"] = head
                statement["predicate"] = chunk.root
                statement["adjectives"] = [token for token in chunk if token.tag_[0: 2] == "JJ"]
                statement["cardinals"] = [token for token in chunk if token.tag_[0: 2] == "CD"]
                statement["complement"] = [token for token in chunk if
                                           token.tag_[0: 2] == "NN" and token.text != chunk.root.text]

                for named_entity in chunk.ents:
                    if named_entity.text == statement["predicate"].text:
                        statement["complement"] += NAMED_ENTITY_MAP[named_entity.label_]

                # print(f'\troot: {chunk.root}')
                # print(f'\thead: {chunk.root.head}  {chunk.root.head.head}')

            # elif chunk.root.head.tag_[0: 2] == "NN":
            #     statement["predicate"] = chunk.root.head
            #     if chunk.root.head.head.tag_[0: 2] == "VB":
            #         statement["verb"] = chunk.root.head.head
            #         # TODO: adjectives

            if bool(statement):
                statements.append(statement)

        statements = list(unique_everseen(statements))

    return statements


def test_statements():
    print()
    statements_generator('which is the largest city in the world?')
    # TODO:
    statements_generator('Show me the most interesting, visited and the most beautiful museums')
    # TODO: but unlisted...
    statements_generator('which are the first 10 artifacts hosted by John Kane but unlisted')
    statements_generator('tell me where the TX\'s location is')
    statements_generator('where the TX\'s location is')
    statements_generator('which is the most interesting museum?')
    statements_generator('give me the artifacts hosted by somebody')
    statements_generator('Show me the most interesting museums in New York')
    statements_generator('How many players from the United States play PG')
