import spacy
from iteration_utilities import unique_everseen

from ro.webdata.nqi.common.constants import SENTENCE_TYPE
from ro.webdata.nqi.common.print_utils import print_statements, print_tokens
from ro.webdata.nqi.nlp.nlp import get_verbs, retokenize
from ro.webdata.nqi.nlp.sentence import get_action, get_cardinals, get_nouns, get_type

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5')


# TODO: lemmatization
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
        "statement_type": SENTENCE_TYPE["MAIN"]\n"
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

        verb_list = [
            {"is_available": True, "is_main": False, "token": verb}
            for verb in get_verbs(sentence)
            if verb.text.lower() not in ["do", "does", "did"]
        ]

        if should_print:
            print_tokens(sentence)
            print(f'\nsentence: {sentence}')
            print_statements(verb_list, 'verb')

        for chunk in document.noun_chunks:
            statement = {
                "action": get_action(document, chunk, verb_list),
                "cardinals": get_cardinals(chunk),
                "nouns": get_nouns(chunk),
                "sentence": chunk,
                "statement_type": get_type(document, chunk)
            }

            # avoid adding a statement which consists only in pronouns or wh-words
            if bool(statement) and statement["statement_type"] not in [SENTENCE_TYPE["PRONOUN"], SENTENCE_TYPE["WH_START"]]:
                statements.append(statement)

        statements = list(unique_everseen(statements))

    return statements
