from spacy.tokens import Span, Token
from ro.webdata.oniq.nlp.nlp_utils import get_next_token, get_wh_words


class Verb:
    """
    Data structure for representing the verbs that are part of an event (Action)

    :attr sentence: The target sentence
    :attr aux_vbs: The list of auxiliary verbs
    :attr main_vb: The main verb
    :attr modal_vb: The modal verb
    """

    def __init__(self, sentence: Span, aux_vbs: [Token] = None, main_vb: Token = None, modal_vb: Token = None):
        self.acomp = _get_acomp(sentence, aux_vbs)
        self.aux_vbs = aux_vbs
        self.main_vb = main_vb
        self.modal_vb = modal_vb

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

    def get_verb(self):
        """
        Get the main verb if it exists, otherwise the auxiliary verb

        :return: The verb
        """

        if self.main_vb is not None:
            return self.main_vb
        return self.aux_vbs


def _get_acomp(sentence: Span, aux_verbs: [Token]):
    """
    Get the adjective if has syntactic dependency of adjectival complement (acomp)

    :param sentence: The target sentence
    :param aux_verbs: The list of auxiliary verbs
    :return: The acomp
    """

    if aux_verbs is None:
        return None

    verb = aux_verbs[len(aux_verbs) - 1]
    next_index = verb.i + 1

    if next_index >= len(sentence):
        return None

    next_word = sentence[next_index]
    if next_word.pos_ == "ADJ" and next_word.dep_ == "acomp":
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
