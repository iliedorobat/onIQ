import logging

from langdetect import detect
from ro.webdata.oniq.common.constants import GLOBAL_ENV, PRINT_MODE


# https://godoc.org/github.com/whitedevops/colors
class COLORS:
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    LIGHT_CYAN = "\033[96m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_RED = "\033[91m"
    RED = "\033[31m"
    RESET_ALL = '\033[0m'


class SYSTEM_MESSAGES:
    METHOD_IS_OBSOLETE = "The method is obsolete and should be updated!"
    METHOD_NOT_TESTED = "The method has not been tested!"
    METHOD_NOT_USED = "The method is not used anymore!"
    METHOD_USED_WITH_SPACY_2 = "The method is intended to be used with Spacy v2"
    VECTORS_NOT_AVAILABLE = f'No vectors are available for word "%s"'


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

    @staticmethod
    def deps_list(document):
        if GLOBAL_ENV.IS_DEBUG and PRINT_MODE.PRINT_DEPS:
            separator = ''
            for i in range(145):
                separator += '-'

            console.info(
                f'{separator}'
                f'\n{"text":{15}}|{"head":{10}}|{"main_head":{10}}|'
                f'{"lefts":{20}}|{"rights":{20}}|'
                f'{"lemma_":{15}}|{"pos_":{10}}|{"tag_":{10}}|{"dep_":{10}}|{"is_stop":{10}}'
            )
            console.info(separator)
            for token in document:
                console.info(
                    f'{token.text:{15}}|{token.head.text:{10}}|{str(token == token.head):{10}}|'
                    f'{str(list(token.lefts)):{20}}|{str(list(token.rights)):{20}}|'
                    f'{token.lemma_:{15}}|{token.pos_:{10}}|{token.tag_:{10}}|{token.dep_:{10}}|{str(token.is_stop):{10}}'
                )
            console.info(separator)
            console.info(f'sentence: {document}')
