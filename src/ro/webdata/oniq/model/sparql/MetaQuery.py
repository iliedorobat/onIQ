import spacy
from iteration_utilities import unique_everseen

from ro.webdata.oniq.common.constants import APP_MODE
from ro.webdata.oniq.common.print_utils import console, echo
from ro.webdata.oniq.model.sparql.Query import Query
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.model.sentence.LogicalOperation import LogicalOperation
from ro.webdata.oniq.nlp.actions import ACTION_EXCEPTIONS, prepare_action_list, get_action
from ro.webdata.oniq.nlp.statements import get_stmt_type
from ro.webdata.oniq.nlp.nlp_utils import get_cardinals, get_preposition, get_prev_chunk, retokenize


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
    def __init__(self, endpoint, nl_query):
        # TODO: nlp("document", disable=["parser"])
        document = nlp(nl_query)
        statements = _prepare_statement_list(document)
        # query = Query(endpoint, statements)
        #
        # self.query = _QUERY_SKELETON.format(
        #     prefixes=Query.get_prefixes(endpoint),
        #     targets=query.get_targets_str(),
        #     where_block=query.get_where_block(),
        #     filter_statement=query.get_filter_block()
        # )
        #
        # if APP_MODE.IS_DEBUG:
        #     print(query)
        #     echo.statements(statements)
        #     print(self.query)
        #
        # # nlp_query = nlp(nl_query)
        # # displacy.serve(nlp_query, style="dep")


def _prepare_statement_list(document):
    """
    TODO: update the documentation
    Build the list of statements\n
    Example of statement:\n
    ...

    :param document: The parsed document
    :return: A list of statements
    """
    statements = []

    for sentence in document.sents:
        retokenize(document, sentence)
        action_list = prepare_action_list(sentence)

        echo.token_list(sentence)
        echo.action_list(action_list)
        console.debug(f'len(action_list) = {len(action_list)}')

        chunks = list(document.noun_chunks)
        for index in range(0, len(chunks)):
            chunk = chunks[index]
            prev_chunk = get_prev_chunk(chunks, index)
            preposition = get_preposition(sentence, chunk)

            console.debug(f'chunks[{index}] = {chunk}')
            console.warning(f'prev_chunk: {prev_chunk}')
            console.warning(f'preposition: {preposition}')

            # TODO: "Which female actor played in Casablanca and is married to a writer born in Rome?"
            # preposition.i > 1 (which of the factors... => preposition.i == 1)
            if preposition is not None and preposition.i > 1:
                start_index = prev_chunk[0].i
                end_index = chunk[len(chunk) - 1].i + 1
                console.error(f'statements[len(statements) - 1].phrase: {statements[len(statements) - 1].phrase}')
                console.error(f'sentence[start_index: end_index]: {sentence[start_index: end_index]}')
                statements[len(statements) - 1].phrase = sentence[start_index: end_index]
            else:
                stmt_type = get_stmt_type(chunk, statements)
                action = get_action(sentence, chunks, index, action_list, statements, stmt_type)
                cardinals = get_cardinals(chunk)
                logical_operation = LogicalOperation(sentence, chunk)
                stmt = Statement(action, cardinals, chunk, logical_operation, statements)
                statements.append(stmt)
                console.error(f'stmt: {stmt.phrase}')

    return _filter_statements(statements)


def _filter_statements(statements):
    statements = list(unique_everseen(statements))
    # avoid adding a statement which consists only in pronouns or wh-words
    return list(
        filter(
            lambda statement: statement.type not in ACTION_EXCEPTIONS, statements
        )
    )
