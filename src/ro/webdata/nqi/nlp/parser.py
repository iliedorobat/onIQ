import spacy
from iteration_utilities import unique_everseen

from ro.webdata.nqi.common.constants import SHOULD_PRINT
from ro.webdata.nqi.common.print_utils import print_actions, print_tokens
from ro.webdata.nqi.nlp.Statement import Statement, get_stmt_type
from ro.webdata.nqi.nlp.nlp_utils import retokenize
from ro.webdata.nqi.nlp.sentence import SENTENCE_TYPE, get_action, get_actions, get_cardinals, get_prev_chunk, get_preposition

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5')


def get_statements(query):
    """
    TODO: update the documentation
    Build the list of statements\n
    Example of statement:\n
    {
        "action": "Find",\n
        "cardinals": [],\n
        "nouns": [\n
            {"dependency": "compound", "is_root": False, "value": "student"},\n
            {"dependency": "dobj", "is_root": True, "value": "name"}\n
        ],\n
        "sentence": "the student name"\n",
        "statement_type": SENTENCE_TYPE["SELECT_CLAUSE"]\n"
    }

    :param query: The query provided by the user in natural language
    :return: A list of statements
    """
    statements = []
    # TODO: nlp("document", disable=["parser"])
    document = nlp(query)

    for sentence in document.sents:
        retokenize(document, sentence)
        actions = get_actions(sentence)

        if SHOULD_PRINT:
            print_tokens(sentence)
            print_actions(actions)

        chunks = list(document.noun_chunks)
        for chunk_index in range(0, len(chunks)):
            chunk = chunks[chunk_index]
            prev_chunk = get_prev_chunk(chunks, chunk_index)
            preposition = get_preposition(sentence, chunk)

            # preposition.i > 1 (which of the factors... => preposition.i == 1)
            if preposition is not None and preposition.i > 1:
                start_index = prev_chunk[0].i
                end_index = chunk[len(chunk) - 1].i + 1
                statements[len(statements) - 1].phrase = sentence[start_index: end_index]
            else:
                stmt_type = get_stmt_type(chunk, statements)
                action = get_action(sentence, chunks, chunk_index, actions, statements, stmt_type)
                cardinals = get_cardinals(chunk)
                statements.append(Statement(action, cardinals, chunk, statements))

    return _filter_statements(statements)


def _filter_statements(statements):
    statements = list(unique_everseen(statements))
    # avoid adding a statement which consists only in pronouns or wh-words
    return list(
        filter(
            lambda statement: statement.type not in [
                # WH_PRONOUN_START ???
                SENTENCE_TYPE["PRONOUN"], SENTENCE_TYPE["WH_START"], SENTENCE_TYPE["WH_PRONOUN_START"]
            ], statements
        )
    )
