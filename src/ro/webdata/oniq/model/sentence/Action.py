import numpy
from spacy.tokens import Span, Token
from ro.webdata.oniq.model.sentence.Adjective import Adjective
from ro.webdata.oniq.model.sentence.Verb import Verb


class Action:
    """
    An event that links two chunks/phrases

    :attr neg: The negation of the event
    :attr verb: An object that contains the main verb, the auxiliary verb(s) and the modal verb
    :attr acomp: The adjectival complement

    E.g.:
        - query: "Which paintings do not have more than three owners?"
        - event: "do not have"
    """

    def __init__(self, sentence: Span, verb: Verb, acomp_list: [Adjective]):
        self.acomp_list = acomp_list
        self.neg = _get_negation(sentence, verb.aux_vbs)
        self.verb = verb

    def __eq__(self, other):
        if not isinstance(other, Action):
            return NotImplemented
        return other is not None and \
            numpy.array_equal(self.acomp_list, other.acomp_list) and \
            self.neg == other.neg and \
            self.verb.__eq__(other.verb)

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        acomp_list = []
        if self.acomp_list is not None:
            for adj in self.acomp_list:
                acomp_list.append(adj.token)
        neg = self.neg if self else None
        verb = self.verb if self else None
        verb_indentation = "\t\t"

        return (
            f'{indentation}action: {{\n'
            f'{indentation}\tneg: {neg},\n'
            f'{indentation}\tverb: {Verb.get_str(verb, verb_indentation)},\n'
            f'{indentation}\tacomp_list: {acomp_list}\n'
            f'{indentation}}}'
        )


def _get_negation(sentence: Span, aux_verbs: [Token]):
    """
    Get the negation of the event (Action)

    :param sentence: The target sentence
    :param aux_verbs: The list of auxiliary verbs
    :return: The negation
    """

    if aux_verbs is None:
        return None

    next_index = aux_verbs[0].i + 1
    if next_index == len(sentence):
        return None

    next_word = sentence[next_index]
    if next_word.dep_ == "neg":
        return next_word

    return None
