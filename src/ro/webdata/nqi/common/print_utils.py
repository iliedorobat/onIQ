import logging

from langdetect import detect


def print_lang_warning(query):
    if detect(query) != "en":
        logging.warning(
            f'\n\tLanguage detected: "{detect(query)}"'
            f'\n\tLanguage required: "en"'
        )


def print_properties(properties):
    for prop in properties:
        print(f'property:    {prop.prop_name_extended}   {prop.ns_name}')


def print_statements(statements, description):
    print()

    for statement in statements:
        print(f'{description}:')

        for key in statement:
            stmt_value = statement[key]
            key = str(key) + ":"

            if isinstance(stmt_value, list) and len(stmt_value) > 0:
                print(f'\t{key}')

                for key_2 in stmt_value:
                    print(f'\t\t{key_2}')
            else:
                print(f'\t{key:{20}} {stmt_value}')

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
