from spacy.tokens import Token

from ro.webdata.oniq.common.constants import PREFIX, QUESTION_TYPES, SEPARATOR
from ro.webdata.oniq.model.rdf.Property import Property


class DEFAULT_TARGET_NAMES:
    LOCATION = "LOCATION"
    TIME = "TIME"
    PERSON = "PERSON"
    THING = "THING"


class Target:
    """
    A word that is used in the SELECT clause

    :attr name: The name of the Target
    :attr prop: TODO
    :attr work: The token that composes the Target

    E.g.: "What museums are in Bacau or Bucharest?"
        - target name: "museum"
        - target word: "museums"
    """

    def __init__(self, word: Token, prop: Property = None):
        self.label = prepare_target_label(word)
        self.prop = prop
        self.word = word

    def __eq__(self, other):
        if not isinstance(other, Target):
            return NotImplemented
        return other is not None and \
            self.label == other.label and \
            self.prop == other.prop and \
            self.word == other.word

    # TODO: implement the __hash__ for all data types
    def __hash__(self):
        return hash((self.label, self.prop, self.word.text))

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}target: {{\n'
            f'{indentation}\tlabel: {self.label},\n'
            f'{indentation}\tprop: {self.prop}\n'
            f'{indentation}\tword: {self.word.text}\n'
            f'{indentation}}}'
        )

    def get_target_name(self, indentation=''):
        var_name = self.label
        if self.prop is not None:
            var_name = self.prop.ns_label + SEPARATOR.STRING + self.prop.prop_name

        return (
            f'{indentation}'
            f'{PREFIX.VARIABLE}{var_name}'
        )


def prepare_target_label(word: Token):
    """
    Prepare the name of the target

    :param word: The token that composes the Target
    :return: The name of the target
    """

    lower = word.lower_

    if lower == QUESTION_TYPES.WHERE:
        return DEFAULT_TARGET_NAMES.LOCATION
    elif lower == QUESTION_TYPES.WHEN:
        return DEFAULT_TARGET_NAMES.TIME
    elif lower in [QUESTION_TYPES.WHO, QUESTION_TYPES.WHOM, QUESTION_TYPES.WHOSE]:
        return DEFAULT_TARGET_NAMES.PERSON
    elif lower == QUESTION_TYPES.WHICH:
        return DEFAULT_TARGET_NAMES.THING
    return word.lemma_
