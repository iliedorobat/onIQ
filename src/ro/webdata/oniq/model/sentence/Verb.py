import numpy
from spacy.tokens import Span, Token
from ro.webdata.oniq.nlp.nlp_utils import get_next_token, get_wh_words
from ro.webdata.oniq.nlp.word_utils import get_prev_word


class Verb:
    """
    Data structure for representing the verbs that are part of an event (Action)

    :attr aux_vbs: The list of auxiliary verbs
    :attr main_vb: The main verb
    :attr modal_vb: The modal verb
    """

    def __init__(self, aux_vbs: [Token] = None, main_vb: Token = None, modal_vb: Token = None):
        self.aux_vbs = aux_vbs
        self.main_vb = main_vb
        self.modal_vb = modal_vb

    def __eq__(self, other):
        if not isinstance(other, Verb):
            return NotImplemented
        return other is not None and \
            numpy.array_equal(self.aux_vbs, other.aux_vbs) and \
            self.main_vb == other.main_vb and \
            self.modal_vb == other.modal_vb

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        aux_vbs = self.aux_vbs if self else None
        main_vb = self.main_vb if self else None
        modal_vb = self.modal_vb if self else None

        return (
            f'{{'
            f'\n{indentation}\taux_vbs: {aux_vbs},'
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
        verb_list = []

        if self.main_vb is not None:
            verb_list.append(self.main_vb)

        if self.modal_vb is not None:
            verb_list.append(self.modal_vb)

        if self.aux_vbs is not None:
            for aux_verb in self.aux_vbs:
                verb_list.append(aux_verb)

        return [token for token in verb_list if token is not None]


def get_main_verb(aux_verb: Token):
    """
    Get the main verb

    E.g.:
        - question: "when was the museum opened?"
            * the verb chain: "was opened" => return "opened"
        - question: "why do they always arrive late?"
            * the verb chain: "do arrive" => return "arrive"
        - question: "when were the panama papers published"
            * the verb chain: "were published" => return "published"
        - question: "where does the holder of the position of Lech Kaczynski live?" [1]
            * the verb chain: "does live" => return "live"

    :param aux_verb: The auxiliary verb
    :return: The main verb or None
    """

    # E.g.: "What is the federated state located in the Weimar Republic?" [1]
    if aux_verb.head == aux_verb:
        prev_word = get_prev_word(aux_verb)

        # E.g.: "Where are the coins and swords located?"
        # E.g.: "When was anıtkabir built?" [3]
        if prev_word is not None and prev_word.lower_ not in ["when", "where"]:
            return None

    next_word = get_next_token(aux_verb, ["DET", "ADV", "ADJ", "ADP", "CCONJ", "NUM", "NOUN", "PRON", "PROPN"])

    # E.g.: "Who is the director who own 2 cars and sold a house or a panel?"
    if next_word is not None and next_word.pos_ == "VERB":
        # TODO: check the old rule: if sentence[next_word.i - 1] not in get_wh_words(sentence):
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

    if not isinstance(sentence, Span) \
            or not isinstance(verb, Token) \
            or verb.pos_ not in ["AUX", "PART"] \
            or verb.i == 0:
        return False

    prev_word = sentence[verb.i - 1]

    if verb.i > 1:
        # 1. E.g.: "Which painting has not been deposited in Bacau?"
        # 2. E.g.: "How many days do I have to wait?"
        # 3. E.g.: "How many days do I have to wait?"
        if (prev_word.pos_ == "PART" and prev_word.dep_ == "neg") or \
                (prev_word.pos_ == "PART" and prev_word.tag_ == "TO") or \
                (prev_word.pos_ == "PRON" and prev_word.dep_ == "nsubj"):
            prev_word = sentence[verb.i - 2]

    if prev_word.pos_ == "AUX":
        return True

    return False
