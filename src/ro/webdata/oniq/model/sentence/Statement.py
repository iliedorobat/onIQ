import numpy
from typing import Union
from spacy.tokens import Doc, Span
from ro.webdata.oniq.common.print_const import COLORS
from ro.webdata.oniq.common.constants import LOGICAL_OPERATIONS
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Conjunction import Conjunction
from ro.webdata.oniq.model.sentence.Phrase import Phrase


class Statement:
    """
    Data structure for representing the relationship between two phrases

    E.g.: "Which paintings are not located in Bacau?"
        - phrase: "Which paintings"
        - action: "are not located"
        - related phrase: "in Bacau"

    :attr phrase_list: The list of phrases generated against the statement
    :attr index: The index of the main phrase for which the statement is built
    :attr action: The event in which the "phrase" is involved
    :attr related_phrase: The phrase which is linked by the "main phrase" through the "action"
    """

    def __init__(self, phrase_list: [Phrase], index: int, action: Action, related_phrase: Phrase):
        self.action = action
        self.phrase = phrase_list[index]
        self.related_phrase = related_phrase
        # self.cardinality = cardinality

    def __eq__(self, other):
        if not isinstance(other, Statement):
            return NotImplemented
        return other is not None and \
            self.action.__eq__(other.action) and \
            self.phrase == other.phrase and \
            self.related_phrase, other.related_phrase

    def __str__(self):
        return self.get_str()

    @staticmethod
    def is_similar_statement(stmt_1, stmt_2):
        has_same_action = stmt_1.action.__eq__(stmt_2.action)
        has_same_target = stmt_1.phrase == stmt_2.phrase
        return has_same_action and has_same_target

    def get_str(self, indentation=''):
        action_indentation = '\t'

        return (
            f'{COLORS.CYAN}'
            f'{indentation}statement: {{\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_CYAN}'
            f'{indentation}\ttarget_phrase: {self.phrase},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_YELLOW}'
            f'{indentation}{Action.get_str(self.action, action_indentation)},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_YELLOW}'
            f'{indentation}\tconjunction: {Conjunction.get_str(self.related_phrase.conj)},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_CYAN}'
            f'{indentation}\trelated_phrases: {self.related_phrase.text}\n'
            f'{COLORS.RESET_ALL}'
        )
