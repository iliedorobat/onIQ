import numpy
import warnings
from spacy.tokens import Span, Token
from ro.webdata.oniq.common.constants import SYSTEM_MESSAGES
from ro.webdata.oniq.model.sentence.Adjective import Adjective
from ro.webdata.oniq.nlp.nlp_utils import get_next_token, get_wh_words


class Verb:
    """
    Data structure for representing the verbs that are part of an event (Action)

    :attr aux_vbs: The list of auxiliary verbs
    :attr main_vb: The main verb
    :attr modal_vb: The modal verb
    :attr acomp: The adjectival complement
    """

    def __init__(self, aux_vbs: [Token] = None, main_vb: Token = None, modal_vb: Token = None, acomp: Adjective = None):
        self.acomp = acomp
        self.aux_vbs = aux_vbs
        self.main_vb = main_vb
        self.modal_vb = modal_vb

    def __eq__(self, other):
        if not isinstance(other, Verb):
            return NotImplemented
        return other is not None and \
            self.acomp == other.acomp and \
            numpy.array_equal(self.aux_vbs, other.aux_vbs) and \
            self.main_vb == other.main_vb and \
            self.modal_vb == other.modal_vb

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        acomp = self.acomp if self else None
        aux_vbs = self.aux_vbs if self else None
        main_vb = self.main_vb if self else None
        modal_vb = self.modal_vb if self else None

        return (
            f'{{'
            f'\n{indentation}\taux_vbs: {aux_vbs},'
            f'\n{indentation}\tacomp: {acomp},'
            f'\n{indentation}\tmain_vb: {main_vb},'
            f'\n{indentation}\tmodal_vb: {modal_vb}'
            f'\n{indentation}}}'
        )

    def has_main_verb(self):
        """
        Check if the instance contains the main_verb

        :return: True if the main_verb != None, otherwise False
        """

        if self.main_vb is not None:
            return True
        return False

    def to_list(self):
        adj_list = self.acomp.to_list() if self.acomp is not None else [None]
        verb_list = [self.main_vb, self.modal_vb]

        if self.aux_vbs is not None:
            for aux_verb in self.aux_vbs:
                verb_list.append(aux_verb)

        return [token for token in adj_list + verb_list if token is not None]


def _get_acomp(sentence: Span, aux_verbs: [Token]):
    """
    Get the adjective if has syntactic dependency of adjectival complement (acomp)

    E.g.:
        - question: "[...] the most beautiful [...]" =>
        - adj: "beautiful"

    :param sentence: The target sentence
    :param aux_verbs: The list of auxiliary verbs
    :return: The adjectival complement
    """

    warnings.warn(SYSTEM_MESSAGES.METHOD_NOT_USED, DeprecationWarning)

    if aux_verbs is None:
        return None

    verb = aux_verbs[len(aux_verbs) - 1]
    next_index = verb.i + 1

    adj_determiner = _get_adj_determiner(sentence, verb)
    if adj_determiner is not None:
        next_index = next_index + 1

    adj_prefix = _get_adj_prefix(sentence, verb)
    if adj_prefix is not None:
        next_index = next_index + 1

    if next_index >= len(sentence):
        return None

    return Adjective(sentence, sentence[next_index])


def _get_adj_determiner(sentence: Span, verb: Token):
    """
    Get the determiner placed before the adjective

    E.g.:
        - question: "[...] the most beautiful [...]" =>
        - determiner: "the"

    :param sentence: The target sentence
    :param verb: The last auxiliary verb
    :return: The determiner (E.g.: "the")
    """

    warnings.warn(SYSTEM_MESSAGES.METHOD_NOT_USED, DeprecationWarning)

    if verb is None:
        return None

    next_index = verb.i + 1
    if next_index >= len(sentence):
        return None

    next_word = sentence[next_index]
    if next_word.pos_ == "DET" and next_word.tag_ == "DT":
        return next_word

    return None


def _get_adj_prefix(sentence: Span, verb: Token):
    """
    Get the superlative/comparative adjective prefix

    E.g.:
        - question: "[...] the most beautiful [...]" =>
        - prefix: "most"

    :param sentence: The target sentence
    :param verb: The last auxiliary verb
    :return: The superlative/comparative adjective prefix (E.g.: "most")
    """

    warnings.warn(SYSTEM_MESSAGES.METHOD_NOT_USED, DeprecationWarning)

    if verb is None:
        return None

    determiner = _get_adj_determiner(sentence, verb)
    next_index = verb.i + 1 if determiner is None else verb.i + 2
    if next_index >= len(sentence):
        return None

    next_word = sentence[next_index]
    if next_word.pos_ == "ADV" and next_word.tag_ in ["RBR", "RBS"]:
        return next_word

    return None


def get_main_verb(sentence: Span, aux_verb: Token):
    """
    Get the main verb

    E.g.:
        - question: "when was the museum opened?"
            * the verb chain: "was opened" => return "opened"
        - question: "why do they always arrive late?"
            * the verb chain: "do arrive" => return "arrive"
        - question: "when were the panama papers published"
            * the verb chain: "were published" => return "published"

    :param sentence: The target sentence
    :param aux_verb: The auxiliary verb
    :return: The main verb or None
    """

    next_word = get_next_token(sentence, aux_verb, ["DET", "ADV", "ADJ", "CCONJ", "NOUN", "PRON", "PROPN"])

    if next_word is not None and next_word.pos_ == "VERB":
        # E.g.: "Who is the director who own 10 cars and sold a house or a panel?"
        if sentence[next_word.i - 1] not in get_wh_words(sentence):
            return next_word

    return None


def is_aux_preceded_by_aux(sentence: Span, verb: Token):
    """
    Check if the auxiliary verb is preceded by another auxiliary verb

    E.g.:
        - question: "which statues do not have more than three owners?"
            * aux ("have") preceded by aux ("do"): "do not have"

    :param sentence: The target sentence
    :param verb: The auxiliary verb
    :return: True/False
    """

    if verb.pos_ != "AUX" or verb.i == 0:
        return False

    prev_word = sentence[verb.i - 1]

    if prev_word.dep_ == "neg" and verb.i > 1:
        prev_word = sentence[verb.i - 2]

    if prev_word.pos_ == "AUX":
        return True

    return False
