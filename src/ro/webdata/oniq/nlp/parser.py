import spacy
from iteration_utilities import unique_everseen

from ro.webdata.oniq.common.print import console, print_token_list
from ro.webdata.oniq.common.print_utils import print_action_list
from ro.webdata.oniq.nlp.sentence.Statement import Statement, get_stmt_type
from ro.webdata.oniq.nlp.sentence.Action import ACTION_EXCEPTIONS, prepare_action_list, get_action
from ro.webdata.oniq.nlp.sentence.utils import get_cardinals, get_conjunction, get_preposition, get_prev_chunk, retokenize

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5')


def get_statements(query):
    """
    TODO: update the documentation
    Build the list of statements\n
    Example of statement:\n
    ...

    :param query: The query provided by the user in natural language
    :return: A list of statements
    """
    statements = []
    # TODO: nlp("document", disable=["parser"])
    document = nlp(query)

    for sentence in document.sents:
        retokenize(document, sentence)
        action_list = prepare_action_list(sentence)

        print_token_list(sentence)
        print_action_list(action_list)
        console.debug(f'len(action_list) = {len(action_list)}')

        chunks = list(document.noun_chunks)
        for index in range(0, len(chunks)):
            chunk = chunks[index]
            console.debug(f'chunks[{index}] = {chunk}')

            prev_chunk = get_prev_chunk(chunks, index)
            preposition = get_preposition(sentence, chunk)

            # preposition.i > 1 (which of the factors... => preposition.i == 1)
            if preposition is not None and preposition.i > 1:
                start_index = prev_chunk[0].i
                end_index = chunk[len(chunk) - 1].i + 1
                statements[len(statements) - 1].phrase = sentence[start_index: end_index]
            else:
                stmt_type = get_stmt_type(chunk, statements)
                action = get_action(sentence, chunks, index, action_list, statements, stmt_type)
                cardinals = get_cardinals(chunk)
                conjunction = get_conjunction(document, chunks, index)
                statements.append(Statement(action, cardinals, chunk, conjunction, statements))

    return _filter_statements(statements)


def _filter_statements(statements):
    statements = list(unique_everseen(statements))
    # avoid adding a statement which consists only in pronouns or wh-words
    return list(
        filter(
            lambda statement: statement.type not in ACTION_EXCEPTIONS, statements
        )
    )
