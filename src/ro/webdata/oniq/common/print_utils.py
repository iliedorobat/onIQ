import logging

from langdetect import detect
from ro.webdata.oniq.nlp.sentence.Action import Action
from ro.webdata.oniq.nlp.sentence.Statement import Statement


def print_lang_warning(query):
    if detect(query) != "en":
        logging.warning(
            f'\n\tLanguage detected: "{detect(query)}"'
            f'\n\tLanguage required: "en"'
        )


def print_properties(properties):
    for prop in properties:
        print(f'property:    {prop.prop_name_extended}   {prop.ns_name}')


def print_statements(statements):
    print()
    for statement in statements:
        print(Statement.get_str(statement))
        print()


def print_actions(actions):
    print()
    for action in actions:
        print(Action.get_str(action))
        print()


def print_tokens(document):
    print(f'--------------------------------------------------------------------------------------------------'
          f'\n{"text":{15}}|{"lemma_":{15}}|{"pos_":{10}}|{"tag_":{10}}|'
          f'{"dep_":{10}}|{"shape_":{10}}|{"is_alpha":{10}}|{"is_stop":{10}}')
    print('--------------------------------------------------------------------------------------------------')
    for token in document:
        print(f'{token.text:{15}}|{token.lemma_:{15}}|{token.pos_:{10}}|{token.tag_:{10}}|{token.dep_:{10}}|'
              f'{token.shape_:{10}}|{token.is_alpha:{10}}|{token.is_stop:{10}}')
    print('--------------------------------------------------------------------------------------------------')
    print(f'sentence: {document}')
