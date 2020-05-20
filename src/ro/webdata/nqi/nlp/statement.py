import spacy
from iteration_utilities import unique_everseen

from ro.webdata.nqi.common.print_utils import print_tokens
from ro.webdata.nqi.nlp.nlp import get_verbs, retokenize
from ro.webdata.nqi.nlp.sentence import get_cardinals, get_nouns, get_type, get_verb

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
        "sentence_type": "main",\n
        "sentence_value": "the student name"\n
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

        if should_print:
            print_tokens(sentence)
            print(f'\nsentence: {sentence}')

        verb_list = [
            {"is_available": True, "token": verb}
            for verb in get_verbs(sentence)
        ]

        for chunk in document.noun_chunks:
            main_sentences = list(filter(lambda item: item["sentence_type"] == "main", statements))
            has_main_sentence = len(main_sentences) > 0

            statement = {
                "action": get_verb(chunk, verb_list),
                "cardinals": get_cardinals(chunk),
                "nouns": get_nouns(chunk),
                "sentence_type": get_type(document, chunk, has_main_sentence),
                "sentence_value": chunk
            }

            if bool(statement):
                statements.append(statement)

        statements = list(unique_everseen(statements))

    return statements
