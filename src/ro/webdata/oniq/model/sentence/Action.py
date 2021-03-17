from spacy.tokens import Span, Token
from ro.webdata.oniq.model.sentence.Verb import Verb


class Action:
    """
    An event that links two chunks/phrases

    :attr dep: The syntactic dependence
    :attr is_available: Specifies if the event (Action) was assigned to a chunk/phrase
    :attr neg: The negation of the event
    :attr verb: An object that contains the main verb, the auxiliary verb(s) and the modal verb
    :attr: i: The index of the first token which composes the event (Action)

    E.g.:
        - query: "Which paintings do not have more than three owners?"
        - event: "do not have"
    """

    def __init__(self, sentence: Span, verb: Verb = None):
        self.dep = _get_dependency(verb)
        self.is_available = True
        self.neg = _get_negation(sentence, verb.aux_vbs)
        self.verb = verb
        self.i = _get_verb_index(self.verb)

    def __eq__(self, other):
        if not isinstance(other, Action):
            return NotImplemented
        return other is not None and \
            self.dep == other.dep and \
            self.is_available == other.is_available and \
            self.neg == other.neg and \
            self.verb.__eq__(other.verb)

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        dep = self.dep if self else None
        is_available = self.is_available if self else None
        neg = self.neg if self else None
        verb = self.verb if self else None
        verb_indentation = "\t\t"

        return (
            f'{indentation}action: {{\n'
            f'{indentation}\tdep: {dep},\n'
            f'{indentation}\tis_available: {is_available},\n'
            f'{indentation}\tneg: {neg},\n'
            f'{indentation}\tverb: {Verb.get_str(verb, verb_indentation)}\n'
            f'{indentation}}}'
        )


def _get_dependency(verb):
    """
    Get the syntactic dependence of the main verb if it exists,
    otherwise of the auxiliary verb

    :param verb: The verb statement
    :return: The syntactic dependency for the action
    """

    if verb.main_vb is not None:
        return verb.main_vb.dep_
    elif verb.aux_vbs is not None:
        last_index = len(verb.aux_vbs) - 1
        return verb.aux_vbs[last_index].dep_
    return None


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


def _get_verb_index(verb: Verb):
    """
    Get the index of the first token which composes the verb
    (which is also the first token which composes the event)

    :param verb: The verb related to the event (Action)
    :return: The index of the first token
    """

    action_verb = verb.main_vb

    # E.g.: Which paintings and statues have not been deposited in Bacau?
    if verb.aux_vbs is not None and len(verb.aux_vbs) > 0:
        action_verb = verb.aux_vbs[0]
    elif verb.modal_vb is not None:
        action_verb = verb.modal_vb

    return action_verb.i if action_verb is not None else -1
