from ro.webdata.oniq.common.constants import IS_DEBUG_MODE, IS_DEBUG_EXTRA_MODE


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
        if IS_DEBUG_MODE:
            print(f'{COLORS.CYAN}{_prepare_message(message, location)}{RESET_ALL}')

    @staticmethod
    def extra_debug(message, location=None):
        if IS_DEBUG_EXTRA_MODE:
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


def print_token_list(document):
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
