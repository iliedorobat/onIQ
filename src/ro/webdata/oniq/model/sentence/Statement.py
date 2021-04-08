from typing import Union
from spacy.tokens import Doc, Span

from ro.webdata.oniq.common.print_const import COLORS
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Phrase import PHRASE_TYPES, Phrase


class Statement:
    """
    Data structure for representing the relationship between two chunks
    """

    def __init__(self, sentence: Union[Doc, Span], target_chunk: Span, action: Action, related_phrase: Span):
        self.action = action
        self.phrase = Phrase(sentence, target_chunk, PHRASE_TYPES.TARGET)
        self.related_phrase = Phrase(sentence, related_phrase, PHRASE_TYPES.RELATED)

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
        phrase_indentation = '\t'

        return (
            f'{indentation}statement: {{\n'
            f'{indentation}{Phrase.get_str(self.phrase, PHRASE_TYPES.TARGET, phrase_indentation)},\n'
            f'{indentation}{Action.get_str(self.action, action_indentation)},\n'
            f'{indentation}{Phrase.get_str(self.related_phrase, PHRASE_TYPES.RELATED, phrase_indentation)}\n'
            f'{indentation}}}'
        )

    def get_str(self, indentation=''):
        action_indentation = '\t'
        phrase_indentation = '\t'

        return (
            f'{COLORS.CYAN}'
            f'{indentation}statement: {{\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_CYAN}'
            f'{indentation}{Phrase.get_str(self.phrase, PHRASE_TYPES.TARGET, phrase_indentation)},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_YELLOW}'
            f'{indentation}{Action.get_str(self.action, action_indentation)},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_CYAN}'
            f'{indentation}{Phrase.get_str(self.related_phrase, PHRASE_TYPES.RELATED, phrase_indentation)}\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.CYAN}'
            f'{indentation}}}'
            f'{COLORS.RESET_ALL}'
        )
