class TEST_MODES:
    DEFAULT = None
    LOCAL_TEST = "local_test"
    GLOBAL_TEST = "global_test"


class GLOBAL_ENV:
    IS_DEBUG = True
    IS_DEBUG_EXTRA = False
    TEST_MODE = TEST_MODES.LOCAL_TEST


class PRINT_MODE:
    PRINT_TOKEN = True
    PRINT_DEPS = True


class LOGICAL_OPERATORS:
    AND = '&&'
    OR = '||'
