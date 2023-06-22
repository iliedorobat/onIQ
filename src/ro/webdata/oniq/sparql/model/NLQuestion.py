import pydash
from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.nlp_utils import text_to_span
from ro.webdata.oniq.common.nlp.sentence_utils import get_root
from ro.webdata.oniq.common.nlp.word_utils import is_aux, is_preceded_by_pass, is_wh_word, is_followed_by_possessive, \
    is_verb, is_noun, get_prev_word, is_aux_pass


class QUESTION_TARGET:
    BOOL = "boolean"
    ENUM = "enumeration"
    LOCATION = "location"  # WHERE
    NUMBER = "number"
    PERSON = "person"  # WHO, WHOM, WHOSE
    THING = "thing"  # others
    TIME = "time"  # WHEN


class QUESTION_TYPES:
    S_AUX = "starts_with_aux"
    S_NOUN = "starts_with_noun"
    S_PREP = "starts_with_prep"
    S_VERB = "starts_with_verb"
    COUNT = "count"  # how many, how much
    HOW = "how"  # how high, how often
    WHEN = "when"
    WHERE = "where"
    WHO = "who"  # who, whom, whose
    WH_OTHERS = "wh_others"
    OTHERS = "others"


class ROOT_TYPES:
    S_AUX = QUESTION_TYPES.S_AUX
    S_NOUN = QUESTION_TYPES.S_NOUN
    S_PREP = QUESTION_TYPES.S_PREP
    S_VERB = QUESTION_TYPES.S_VERB
    AUX = "auxiliary_verb"  # The root of the question is an aux verb
    MAIN = "main_verb"  # The question ends with a verb
    PASSIVE = "passive"  # The question ends with a verb which has a passive verb attached
    PASSIVE_NEAR = "passive_near"
    POSSESSIVE = "possessive"
    POSSESSIVE_COMPLEX = "possessive_complex"
    OTHERS = "others"


class NLQuestion:
    def __init__(self, input_question: str):
        question = text_to_span(input_question)

        self.main_type = _get_question_type(question)
        self.target = _get_question_target(question)
        self.root_type = _get_root_type(question)
        self.question = question

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
    def starts_with_noun(question: Span):
        if not isinstance(question, Span):
            return False

        start_word = pydash.get(question, "0")

        return is_noun(start_word)

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
        # E.g.: "Did Arnold Schwarzenegger attend a university?"
        return QUESTION_TYPES.S_AUX
    elif NLQuestion.starts_with_verb(question):
        # E.g.: "Give me the currency of China."
        return QUESTION_TYPES.S_VERB
    elif NLQuestion.starts_with_noun(question):
        # E.g.: "Desserts from which country contain fish?"
        return QUESTION_TYPES.S_NOUN
    elif NLQuestion.starts_with_prep(question):
        # E.g.: "At what distance does the earth curve?"
        # E.g.: "In which country is Mecca located?"
        return QUESTION_TYPES.S_PREP
    elif NLQuestion.starts_with_wh(question):
        first_word = pydash.get(question, "0")

        if isinstance(first_word, Token):
            first_word = first_word.lower_

            if first_word in ["who", "whom", "whose"]:
                return QUESTION_TYPES.WHO
            elif first_word == "when":
                return QUESTION_TYPES.WHEN
            elif first_word == "where":
                return QUESTION_TYPES.WHERE
            elif first_word == "how":
                if len(question) > 1 and question[1].lower_ in ["many", "much"]:
                    # E.g.: "How many ethnic groups live in Slovenia?"
                    return QUESTION_TYPES.COUNT

                # E.g.: "How high is the Yokohama Marine Tower?"
                return QUESTION_TYPES.HOW

        return QUESTION_TYPES.WH_OTHERS

    return QUESTION_TYPES.OTHERS


def _get_root_type(question: Span):
    if not isinstance(question, Span) or len(question) < 2:
        return None

    if NLQuestion.starts_with_aux(question):
        # E.g.: "Did Arnold Schwarzenegger attend a university?"
        return ROOT_TYPES.S_AUX
    elif NLQuestion.starts_with_verb(question):
        # E.g.: "Give me the currency of China."
        return ROOT_TYPES.S_VERB
    elif NLQuestion.starts_with_noun(question):
        # E.g.: "Desserts from which country contain fish?"
        return ROOT_TYPES.S_NOUN
    elif NLQuestion.starts_with_prep(question):
        # E.g.: "At what distance does the earth curve?"
        # E.g.: "In which country is Mecca located?"
        return ROOT_TYPES.S_PREP
    elif NLQuestion.starts_with_wh(question):
        main_head = get_root(question)

        if is_aux(main_head):
            if NLQuestion.is_poss_question(question):
                if is_followed_by_possessive(main_head):
                    # E.g.: "Who is the person whose successor was Le Hong Phong?"
                    return ROOT_TYPES.POSSESSIVE_COMPLEX

                # E.g.: ### "Whose successor is Le Hong Phong?"
                return ROOT_TYPES.POSSESSIVE

            # E.g.: "Who is the leader of the town where the Myntdu river originates?"
            return ROOT_TYPES.AUX
        elif is_preceded_by_pass(main_head):
            prev_word = get_prev_word(main_head)

            if is_aux_pass(prev_word):
                # E.g.: "Who was married to an actor that played in Philadelphia?"
                # E.g.: "Which soccer players were born on Malta?"
                return ROOT_TYPES.PASSIVE_NEAR

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
    elif question_type == QUESTION_TYPES.WHO:
        return QUESTION_TARGET.PERSON

    elif question_type == QUESTION_TYPES.S_AUX:
        return QUESTION_TARGET.BOOL
    elif question_type in [QUESTION_TYPES.S_NOUN, QUESTION_TYPES.S_VERB]:
        return QUESTION_TARGET.ENUM
    elif question_type == QUESTION_TYPES.COUNT:
        return QUESTION_TARGET.NUMBER

    return QUESTION_TARGET.THING
