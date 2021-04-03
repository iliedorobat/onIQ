from typing import Union
from spacy.tokens import Doc, Span

from ro.webdata.oniq.common.print_const import COLORS
from ro.webdata.oniq.common.constants import LOGICAL_OPERATIONS
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Phrase import Phrase
from ro.webdata.oniq.model.sentence.Conjunction import Conjunction


class Statement:
    """
    Data structure for representing the relationship between two chunks
    """

    def __init__(self, sentence: Union[Doc, Span], target_chunk: Span, action: Action, related_phrase: Span):
        self.action = action
        self.phrase = Phrase(sentence, target_chunk)
        self.related_phrase = Phrase(sentence, related_phrase)
        # TODO: add phrase-level conjunction (in Phrase)
        self.conj = self.related_phrase.conj if self.related_phrase.conj is not None else None

    def __eq__(self, other):
        if not isinstance(other, Statement):
            return NotImplemented
        return other is not None and \
            self.action.__eq__(other.action) and \
            self.phrase == other.phrase and \
            self.related_phrase, other.related_phrase

    def __str__(self):
        return self.get_str()

    def get_basic_str(self, indentation=''):
        action_indentation = '\t'
        related_phrase = self.related_phrase.text if self.related_phrase is not None else None
        conjunction = Conjunction.get_str(self.conj) if self.conj is not None else None

        return (
            f'{indentation}statement: {{\n'
            f'{indentation}\ttarget_chunk: {self.phrase},\n'
            f'{indentation}{Action.get_str(self.action, action_indentation)},\n'
            f'{indentation}\tconjunction: {conjunction},\n'
            f'{indentation}\trelated_phrase: {related_phrase}\n'
            f'{indentation}}}'
        )

    def get_str(self, indentation=''):
        action_indentation = '\t'
        related_phrase = self.related_phrase.text if self.related_phrase is not None else None
        conjunction = Conjunction.get_str(self.conj) if self.conj is not None else None

        return (
            f'{COLORS.CYAN}'
            f'{indentation}statement: {{\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_CYAN}'
            f'{indentation}\ttarget_chunk: {self.phrase.text},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_YELLOW}'
            f'{indentation}{Action.get_str(self.action, action_indentation)},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_YELLOW}'
            f'{indentation}\tconjunction: {conjunction},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_CYAN}'
            f'{indentation}\trelated_phrase: {related_phrase}\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.CYAN}'
            f'{indentation}}}'
            f'{COLORS.RESET_ALL}'
        )
