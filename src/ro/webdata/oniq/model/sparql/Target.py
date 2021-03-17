from spacy.tokens import Token
from ro.webdata.oniq.common.constants import PREFIX, SEPARATOR


class Target:
    """
    A word that is used in the SELECT clause

    :attr name: The name of the Target
    :attr work: The token that composes the Target

    E.g.: "What museums are in Bacau or Bucharest?"
        - target name: "museum"
        - target word: "museums"
    """

    def __init__(self, word: Token):
        self.name = _prepare_name(word)
        self.word = word

    def __eq__(self, other):
        if not isinstance(other, Target):
            return NotImplemented
        return other is not None and \
            self.name == other.name and \
            self.word == other.word

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}target: {{\n'
            f'{indentation}\tname: {self.name},\n'
            f'{indentation}\tword: {self.word.text}\n'
            f'{indentation}}}'
        )

    def get_variable_pattern(self, indentation=''):
        return (
            f'{indentation}'
            f'{PREFIX.VARIABLE}{self.name}{SEPARATOR.TRIPLE_PATTERN}'
        )


def _prepare_name(word: Token):
    """
    Prepare the name of the target

    :param word: The token that composes the Target
    :return: The name of the target
    """

    lower = word.lower_

    if lower == "where":
        return "LOCATION"
    elif lower == "when":
        return "TIME"
    elif lower in ["who", "whose"]:
        return "PERSON"
    elif lower == "which":
        return "THING"
    return word.lemma_
