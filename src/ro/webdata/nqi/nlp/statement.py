import spacy
from iteration_utilities import unique_everseen

from ro.webdata.nqi.common.constants import PRONOUNS, SENTENCE_TYPE
from ro.webdata.nqi.common.print_utils import print_statements, print_tokens
from ro.webdata.nqi.nlp.nlp_utils import get_wh_adverbs, get_wh_pronouns, get_wh_words, retokenize
from ro.webdata.nqi.nlp.sentence import get_action, get_actions, get_cardinals, get_nouns, get_preposition

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5')


def get_statements(query, should_print=False):
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
    :param should_print: A flag which specify if additional information should be printed
    :return: A list of statements
    """
    statements = []
    # TODO: nlp("document", disable=["parser"])
    document = nlp(query)

    for sentence in document.sents:
        retokenize(document, sentence)
        actions = get_actions(sentence)

        if should_print:
            print_tokens(sentence)
            print_statements(actions, 'actions')

        chunks = list(document.noun_chunks)
        for chunk_index in range(0, len(chunks)):
            chunk = chunks[chunk_index]
            prev_chunk = get_prev_chunk(chunks, chunk_index)
            preposition = get_preposition(sentence, chunk)

            # preposition.i > 1 (which of the museums... => preposition.i == 1)
            if preposition is not None and preposition.i > 1:
                start_index = prev_chunk[0].i
                end_index = chunk[len(chunk) - 1].i + 1
                statements[len(statements) - 1]["phrase"] = sentence[start_index: end_index]
            else:
                cardinals = get_cardinals(chunk)
                statement_type = get_statement_type(chunk, statements)
                # TODO: move the statement_type inside of get_action method
                action = get_action(sentence, chunks, chunk_index, actions, statements, statement_type)

                statements.append({
                    "action": action,
                    "cardinals": cardinals,
                    "phrase": chunk,
                    "statement_type": statement_type
                })

    statements = list(unique_everseen(statements))
    # avoid adding a statement which consists only in pronouns or wh-words
    statements = list(
        filter(
            lambda statement: statement["statement_type"] not in [
                # WH_PRONOUN_START ???
                SENTENCE_TYPE["PRONOUN"], SENTENCE_TYPE["WH_START"], SENTENCE_TYPE["WH_PRONOUN_START"]
            ], statements
        )
    )

    return statements


def get_prev_chunk(chunks, chunk_index):
    if chunk_index > 0:
        return chunks[chunk_index - 1]
    return None


def get_statement_type(chunk, statements):
    if chunk.text.lower() in PRONOUNS:
        return SENTENCE_TYPE["PRONOUN"]
    # "who is the director who own..." => classify only the first chunk which contains
    # the "who" word as being WH_PRONOUN_START
    elif chunk.root in get_wh_pronouns(chunk):
        if chunk.root.i == 0:
            return SENTENCE_TYPE["WH_PRONOUN_START"]
        else:
            return SENTENCE_TYPE["WH_START"]
    elif chunk.root in get_wh_words(chunk) and chunk.root.i == 0:
        return SENTENCE_TYPE["WH_START"]
    # if the type of the first sentence is not SENTENCE_TYPE["PRONOUN"] or SENTENCE_TYPE["WH_START"],
    # then the target subjects are found in the first sentence
    elif len(statements) == 0:
        return SENTENCE_TYPE["SELECT_CLAUSE"]
    else:
        nouns = get_nouns(chunk)
        conj_nouns = list(filter(lambda noun: noun["dependency"] == "conj", nouns))
        prev_statement = get_last_statement(statements)

        if prev_statement["statement_type"] in [SENTENCE_TYPE["PRONOUN"], SENTENCE_TYPE["WH_START"], SENTENCE_TYPE["WH_PRONOUN_START"]]:
            return SENTENCE_TYPE["SELECT_CLAUSE"]
        elif prev_statement["statement_type"] == SENTENCE_TYPE["SELECT_CLAUSE"] and len(conj_nouns) > 0:
            return SENTENCE_TYPE["SELECT_CLAUSE"]
        else:
            return SENTENCE_TYPE["WHERE_CLAUSE"]


def get_last_statement(statements):
    if len(statements) > 0:
        return statements[len(statements) - 1]
    return None

