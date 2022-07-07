import logging

from langdetect import detect
from ro.webdata.oniq.common.constants import GLOBAL_ENV, PRINT_MODE
from ro.webdata.oniq.common.print_const import COLORS
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.model.sparql.Target import Target


# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python#answer-287944
class console:
    @staticmethod
    def debug(message, location=None):
        if GLOBAL_ENV.IS_DEBUG:
            print(f'{COLORS.CYAN}{_prepare_message(message, location)}{COLORS.RESET_ALL}')

    @staticmethod
    def extra_debug(message, location=None):
        if GLOBAL_ENV.IS_DEBUG_EXTRA:
            print(f'{COLORS.CYAN}{_prepare_message(message, location)}{COLORS.RESET_ALL}')

    @staticmethod
    def log(message, location=None):
        print(f'{COLORS.BLUE}{_prepare_message(message, location)}{COLORS.RESET_ALL}')

    @staticmethod
    def info(message, location=None):
        print(f'{COLORS.LIGHT_CYAN}{_prepare_message(message, location)}{COLORS.RESET_ALL}')

    @staticmethod
    def warning(message, location=None):
        print(f'{COLORS.LIGHT_YELLOW}{_prepare_message(message, location)}{COLORS.RESET_ALL}')

    @staticmethod
    def error(message, location=None):
        print(f'{COLORS.RED}{_prepare_message(message, location)}{COLORS.RESET_ALL}')


def _prepare_message(message, location=None):
    if location is None:
        return message
    else:
        return str(location) + ': ' + message


class echo:
    @staticmethod
    def action_list(actions):
        if GLOBAL_ENV.IS_DEBUG and PRINT_MODE.PRINT_ACTION:
            print(f'\nlen(action_list) = {len(actions)}\n')
            for action in actions:
                print(Action.get_str(action))
                print()

    @staticmethod
    def lang_warning(query):
        if detect(query) != "en":
            logging.warning(
                f'\n\tLanguage detected: "{detect(query)}"'
                f'\n\tLanguage required: "en"'
            )

    @staticmethod
    def properties(properties):
        if GLOBAL_ENV.IS_DEBUG:
            for prop in properties:
                print(f'property:    {prop.prop_name_extended}   {prop.ns_name}')

    @staticmethod
    def statement_list(statements):
        if GLOBAL_ENV.IS_DEBUG and PRINT_MODE.PRINT_STATEMENT:
            print()
            for statement in statements:
                print(Statement.get_str(statement))

    @staticmethod
    def target_list(targets: [Target]):
        if GLOBAL_ENV.IS_DEBUG and PRINT_MODE.PRINT_TARGET:
            print()
            for target in targets:
                print(target)

    @staticmethod
    def token_list(document):
        if GLOBAL_ENV.IS_DEBUG and PRINT_MODE.PRINT_TOKEN:
            console.info(
                f'-------------------------------------------------------------------------------------------------------'
                f'\n{"text":{15}}|{"lemma_":{15}}|{"pos_":{10}}|{"tag_":{10}}|'
                f'{"dep_":{10}}|{"shape_":{15}}|{"is_alpha":{10}}|{"is_stop":{10}}'
            )
            console.info(
                '-------------------------------------------------------------------------------------------------------'
            )
            for token in document:
                console.info(
                    f'{token.text:{15}}|{token.lemma_:{15}}|{token.pos_:{10}}|{token.tag_:{10}}|{token.dep_:{10}}|'
                    f'{token.shape_:{15}}|{token.is_alpha:{10}}|{token.is_stop:{10}}'
                )
            console.info(
                '-------------------------------------------------------------------------------------------------------'
            )
            console.info(f'sentence: {document}')
