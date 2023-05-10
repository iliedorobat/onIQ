import pydash
from spacy.tokens import Span

from ro.webdata.oniq.common.nlp.word_utils import is_aux, is_preceded_by_pass, is_wh_word, is_followed_by_possessive, is_verb
from ro.webdata.oniq.common.nlp.sentence_utils import get_root


class QUESTION_TARGET:
    LOCATION = "location"  # WHERE
    PERSON = "person"  # WHO, WHOM, WHOSE
    THING = "thing"  # others
    TIME = "time"  # WHEN


# TODO: complete the list
class QUESTION_TYPES:
    AUX_ASK = "aux_ask"  # E.g.: "Is rizal monument a place?"
    PREP_ASK = "prep_ask"  # E.g.: "In which country is Mecca located?"
    # COUNT = "count"  # how many, how much, how often
    HOW = "how"
    WHAT = "what"
    WHEN = "when"
    WHERE = "where"
    WHICH = "which"
    WHO = "who"
    WHOM = "whom"
    WHOSE = "whose"
    WHY = "why"
    OTHERS = "others"


class ROOT_TYPES:
    AUX = "auxiliary_verb"  # The root of the question is an aux verb
    AUX_ASK = "aux_ask"  # The question starts with an aux verb
    MAIN = "main_verb"  # The question ends with a verb
    PASSIVE = "passive"  # The question ends with a verb which has a passive verb attached
    POSSESSIVE = "possessive"
    POSSESSIVE_COMPLEX = "possessive_complex"
    PREP_ASK = "prep_ask"
    VERB_ASK = "verb_ask"  # The question starts with a verb
    OTHERS = "others"


class NLQuestion:
    def __init__(self, question: Span):
        self.main_type = _get_question_type(question)
        self.target = _get_question_target(question)
        self.root_type = _get_root_type(question)
        self.value = question

    @staticmethod
    def is_poss_question(question: Span):
        if not isinstance(question, Span):
            return False

        for token in question:
            if token.dep_ == "poss":
                return True

        return False

    @staticmethod
    def starts_with_aux(question: Span):
        if not isinstance(question, Span):
            return False

        start_word = pydash.get(question, "0")

        return is_aux(start_word)

    @staticmethod
    def starts_with_prep(question: Span):
        if not isinstance(question, Span):
            return False

        # E.g.: "At what distance does the earth curve?"
        # E.g.: "In which country is Mecca located?"
        start_word = pydash.get(question, "0")
        second_word = pydash.get(question, "1")

        return start_word.dep_ == "prep" and is_wh_word(second_word)

    @staticmethod
    def starts_with_verb(question: Span):
        if not isinstance(question, Span):
            return False

        start_word = pydash.get(question, "0")

        return is_verb(start_word)

    @staticmethod
    def starts_with_wh(question: Span):
        if not isinstance(question, Span):
            return False

        start_word = pydash.get(question, "0")

        return is_wh_word(start_word)


def _get_question_type(question: Span):
    if not isinstance(question, Span) or len(question) == 0:
        return None

    if NLQuestion.starts_with_aux(question):
        return QUESTION_TYPES.AUX_ASK
    elif NLQuestion.starts_with_prep(question):
        return QUESTION_TYPES.PREP_ASK
    elif NLQuestion.starts_with_wh(question):
        first_word = pydash.get(question, "0")
        return getattr(QUESTION_TYPES, first_word.text.upper())

    return QUESTION_TYPES.OTHERS


def _get_root_type(question: Span):
    if not isinstance(question, Span) or len(question) < 2:
        return None

    if NLQuestion.starts_with_aux(question):
        # E.g.: "Did Arnold Schwarzenegger attend a university?"
        return ROOT_TYPES.AUX_ASK
    elif NLQuestion.starts_with_verb(question):
        # E.g.: "Give me the currency of China."
        return ROOT_TYPES.VERB_ASK
    elif NLQuestion.starts_with_prep(question):
        # E.g.: "At what distance does the earth curve?"
        # E.g.: "In which country is Mecca located?"
        return ROOT_TYPES.PREP_ASK
    elif NLQuestion.starts_with_wh(question):
        main_head = get_root(question)

        if is_aux(main_head):
            if NLQuestion.is_poss_question(question):
                if is_followed_by_possessive(main_head):
                    # E.g.: "Who is the person whose successor was Le Hong Phong?"
                    return ROOT_TYPES.POSSESSIVE_COMPLEX

                # E.g.: "Whose successor is Le Hong Phong?"  ## made by me
                return ROOT_TYPES.POSSESSIVE

            # E.g.: "Who is the leader of the town where the Myntdu river originates?"
            return ROOT_TYPES.AUX
        elif is_preceded_by_pass(main_head):
            # E.g.: ### "where was the person who won the oscar born?"
            return ROOT_TYPES.PASSIVE
        else:
            # E.g.: "Where did Mashhur bin Abdulaziz Al Saud's father die?"
            return ROOT_TYPES.MAIN

    return ROOT_TYPES.OTHERS


def _get_question_target(question: Span):
    question_type = _get_question_type(question)

    if question_type == QUESTION_TYPES.WHEN:
        return QUESTION_TARGET.TIME
    elif question_type == QUESTION_TYPES.WHERE:
        return QUESTION_TARGET.LOCATION
    elif question_type in [QUESTION_TYPES.WHO, QUESTION_TYPES.WHOM, QUESTION_TYPES.WHOSE]:
        return QUESTION_TARGET.PERSON
    return QUESTION_TARGET.THING
