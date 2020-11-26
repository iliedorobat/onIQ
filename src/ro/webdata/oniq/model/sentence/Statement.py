from ro.webdata.oniq.common.constants import LOGICAL_OPERATIONS
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.LogicalOperation import LogicalOperation
from ro.webdata.oniq.nlp.nlp_utils import get_wh_words


class Statement:
    def __init__(self, action, cardinality, phrase, logical_operation, statements):
        self.action = action
        self.cardinality = cardinality
        self.logical_operation = logical_operation
        self.phrase = phrase
        self.wh_word = _prepare_wh_word(phrase, logical_operation, statements)

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        action_indentation = '\t'

        return (
            f'{indentation}statement: {{\n'
            f'{indentation}{Action.get_str(self.action, action_indentation)},\n'
            f'{indentation}\tcardinality: {self.cardinality},\n'
            f'{indentation}\t{LogicalOperation.get_str(self.logical_operation)},\n'
            f'{indentation}\tphrase: {self.phrase},\n'
            f'{indentation}\twh_word: {self.wh_word}\n'
            f'{indentation}}}'
        )


def _prepare_wh_word(phrase, logical_operation, statements):
    if logical_operation is not None and logical_operation.name in [LOGICAL_OPERATIONS.AND, LOGICAL_OPERATIONS.AND]:
        last_stmt = statements[len(statements) - 1]
        return last_stmt.wh_word
    return _get_wh_word(phrase)


def _get_wh_word(phrase):
    if phrase is None:
        return None

    # [...] and [...] one of the [...]
    #      CCONJ      NUM ADP DET
    pos_list = ["ADJ", "ADV", "NOUN", "PRON"] + ["ADP", "CCONJ", "DET", "NUM", "PUNCT"]
    wh_words = get_wh_words(phrase)

    for i in reversed(range(len(phrase))):
        token = phrase[i]
        if token in wh_words:
            return phrase[token.i: token.i + 1]
        elif token.pos_ not in pos_list:
            return phrase[0: i + 1]

    return None
