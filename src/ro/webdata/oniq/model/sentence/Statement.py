from ro.webdata.oniq.common.print_const import COLORS
from ro.webdata.oniq.common.constants import LOGICAL_OPERATIONS
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.LogicalOperation import LogicalOperation
from ro.webdata.oniq.nlp.nlp_utils import get_wh_words


class Statement:
    """
    Data structure for representing the relationship between two phrases

    E.g.: "Which paintings are not located in Bacau?"
        - phrase: "Which paintings"
        - action: "are not located"
        - related phrase: "in Bacau"

    :attr phrase: The main phrase for which the statement is built
    :attr action: The event in which the "phrase" is involved
    :attr related_phrase: The phrase which is linked by the "main phrase" through the "action"
    """

    def __init__(self, phrase, action, related_phrase):
        self.action = action
        self.phrase = phrase
        self.related_phrase = related_phrase

        # self.cardinality = cardinality
        # self.logical_operation = logical_operation
        # self.wh_word = _prepare_wh_word(phrase, logical_operation, statements)

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        action_indentation = '\t'

        return (
            f'{COLORS.CYAN}'
            f'{indentation}statement: {{\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_CYAN}'
            f'{indentation}\tphrase: {self.phrase},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_YELLOW}'
            f'{indentation}{Action.get_str(self.action, action_indentation)},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_CYAN}'
            f'{indentation}\trelated_phrase: {self.related_phrase},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.CYAN}'
            # f'{indentation}\tcardinality: {self.cardinality},\n'
            # f'{indentation}\t{LogicalOperation.get_str(self.logical_operation)},\n'
            f'{indentation}}}'
            f'{COLORS.RESET_ALL}'
        )
