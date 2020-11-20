import logging

from langdetect import detect
from ro.webdata.oniq.common.constants import IS_DEBUG_MODE
from ro.webdata.oniq.nlp.sentence.Action import Action
from ro.webdata.oniq.nlp.sentence.Statement import Statement


def print_lang_warning(query):
    if detect(query) != "en":
        logging.warning(
            f'\n\tLanguage detected: "{detect(query)}"'
            f'\n\tLanguage required: "en"'
        )


def print_properties(properties):
    if IS_DEBUG_MODE:
        for prop in properties:
            print(f'property:    {prop.prop_name_extended}   {prop.ns_name}')


def print_statements(statements):
    if IS_DEBUG_MODE:
        print()
        for statement in statements:
            print(Statement.get_str(statement))
            print()


def print_action_list(actions):
    if IS_DEBUG_MODE:
        print()
        for action in actions:
            print(Action.get_str(action))
            print()
