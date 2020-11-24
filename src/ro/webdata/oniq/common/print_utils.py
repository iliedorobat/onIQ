import logging

from langdetect import detect
from ro.webdata.oniq.common.constants import APP_MODE
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Statement import Statement


RESET_ALL = '\033[0m'


# https://godoc.org/github.com/whitedevops/colors
class COLORS:
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    LIGHT_CYAN = "\033[96m"
    LIGHT_YELLOW = "\033[93m"
    RED = "\033[31m"


# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python#answer-287944
class console:
    @staticmethod
    def debug(message, location=None):
        if APP_MODE.IS_DEBUG:
            print(f'{COLORS.CYAN}{_prepare_message(message, location)}{RESET_ALL}')

    @staticmethod
    def extra_debug(message, location=None):
        if APP_MODE.IS_DEBUG_EXTRA:
            print(f'{COLORS.CYAN}{_prepare_message(message, location)}{RESET_ALL}')

    @staticmethod
    def log(message, location=None):
        print(f'{COLORS.BLUE}{_prepare_message(message, location)}{RESET_ALL}')

    @staticmethod
    def info(message, location=None):
        print(f'{COLORS.LIGHT_CYAN}{_prepare_message(message, location)}{RESET_ALL}')

    @staticmethod
    def warning(message, location=None):
        print(f'{COLORS.LIGHT_YELLOW}{_prepare_message(message, location)}{RESET_ALL}')

    @staticmethod
    def error(message, location=None):
        print(f'{COLORS.RED}{_prepare_message(message, location)}{RESET_ALL}')


def _prepare_message(message, location=None):
    if location is None:
        return message
    else:
        return str(location) + ': ' + message


class echo:
    @staticmethod
    def action_list(actions):
        if APP_MODE.IS_DEBUG:
            print()
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
        if APP_MODE.IS_DEBUG:
            for prop in properties:
                print(f'property:    {prop.prop_name_extended}   {prop.ns_name}')

    @staticmethod
    def statements(statements):
        if APP_MODE.IS_DEBUG:
            print()
            for statement in statements:
                print(Statement.get_str(statement))
                print()

    @staticmethod
    def token_list(document):
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
