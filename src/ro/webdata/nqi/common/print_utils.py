import logging

from langdetect import detect
from ro.webdata.nqi.nlp.Action import Action


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
        print("statement:")

        keys = list([
            attr for attr in dir(statement)
            if not callable(getattr(statement, attr)) and not attr.startswith("__")
        ])

        for key in keys:
            stmt_value = statement.__dict__[key]
            key = str(key) + ":"

            if isinstance(stmt_value, list) and len(stmt_value) > 0:
                print(f'\t{key}')

                for key_2 in stmt_value:
                    print(f'\t\t{key_2}')
            else:
                if isinstance(stmt_value, Action):
                    print_action(stmt_value, '\t')
                else:
                    print(f'\t{key:{20}} {stmt_value}')

        print()


def print_actions(actions):
    print()

    for action in actions:
        print_action(action)


def print_action(action, indentation=''):
    print(Action.get_str(action, indentation))
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
