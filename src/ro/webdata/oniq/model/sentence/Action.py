from spacy.tokens import Span, Token
from ro.webdata.oniq.model.sentence.Adjective import Adjective
from ro.webdata.oniq.model.sentence.Verb import Verb


class Action:
    """
    An event that links two chunks/phrases

    TODO :attr adj: move the adjective to the Noun
    :attr dep: the syntactic dependence
    :attr is_available: a flag that specifies if the action was assigned to a chunk/phrase
    :attr neg: The negation of the event
    :attr verb: an object that contains the main verb, the auxiliary verb(s) and the modal verb

    E.g.:
        - query: "Which paintings do not have more than three owners?"
        - event: "do not have"
    """

    def __init__(self, sentence: Span, verb: Verb = None, adj: Adjective = None):
        self.adj = adj
        self.dep = _get_dependency(verb)
        self.is_available = True
        self.neg = _get_negation(sentence, verb.aux_vbs)
        self.verb = verb

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        adj = self.adj if self else None
        dep = self.dep if self else None
        is_available = self.is_available if self else None
        neg = self.neg if self else None
        verb = self.verb if self else None
        verb_indentation = "\t"

        return (
            f'{indentation}action: {{\n'
            f'{indentation}\tdep: {dep},\n'
            f'{indentation}\tis_available: {is_available},\n'
            f'{indentation}\tadj: {adj},\n'
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
