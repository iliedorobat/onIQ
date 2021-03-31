from spacy.tokens import Span
from ro.webdata.oniq.common.print_const import COLORS
from ro.webdata.oniq.common.constants import LOGICAL_OPERATIONS
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Conjunction import Conjunction


class Statement:
    """
    Data structure for representing the relationship between two chunks
    """

    def __init__(self, target_chunks: [Span], action: Action, related_chunk: Span):
        self.action = action
        self.chunks = target_chunks
        self.related_chunk = related_chunk
        # TODO: self.conj = _prepare_conjunction(self.phrase, self.related_chunk)

    def __eq__(self, other):
        if not isinstance(other, Statement):
            return NotImplemented
        return other is not None and \
            self.action.__eq__(other.action) and \
            self.chunks == other.chunks and \
            self.related_chunk, other.related_chunk

    def __str__(self):
        return self.get_str()

    def get_basic_str(self, indentation=''):
        action_indentation = '\t'
        related_chunk = self.related_chunk.text if self.related_chunk is not None else None

        return (
            f'{indentation}statement: {{\n'
            f'{indentation}\ttarget_chunks: {self.chunks},\n'
            f'{indentation}{Action.get_str(self.action, action_indentation)},\n'
            # f'{indentation}\tconjunction: {Conjunction.get_str(self.conj)},\n'
            f'{indentation}\trelated_chunk: {related_chunk}\n'
            f'{indentation}}}'
        )

    def get_str(self, indentation=''):
        action_indentation = '\t'
        related_chunk = self.related_chunk.text if self.related_chunk is not None else None

        return (
            f'{COLORS.CYAN}'
            f'{indentation}statement: {{\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_CYAN}'
            f'{indentation}\ttarget_chunks: {self.chunks},\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_YELLOW}'
            f'{indentation}{Action.get_str(self.action, action_indentation)},\n'
            f'{COLORS.RESET_ALL}'

            # f'{COLORS.LIGHT_YELLOW}'
            # f'{indentation}\tconjunction: {Conjunction.get_str(self.conj)},\n'
            # f'{COLORS.RESET_ALL}'

            f'{COLORS.LIGHT_CYAN}'
            f'{indentation}\trelated_chunk: {related_chunk}\n'
            f'{COLORS.RESET_ALL}'

            f'{COLORS.CYAN}'
            f'{indentation}}}'
            f'{COLORS.RESET_ALL}'
        )
