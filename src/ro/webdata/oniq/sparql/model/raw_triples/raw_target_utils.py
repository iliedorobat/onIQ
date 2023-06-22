from typing import List

from spacy.tokens import Span

from ro.webdata.oniq.common.nlp.word_utils import is_noun
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, SYNTACTIC_TYPES, QUESTION_TARGET, QUESTION_TYPES
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class RawTargetUtils:
    @staticmethod
    def update_target_nouns(nl_question: NLQuestion, target_nouns: List[NounEntity], raw_triple: RawTriple):
        new_target_tokens = _get_target_tokens(nl_question, nl_question.question)

        # ORDER IS CRUCIAL
        if nl_question.question_type == QUESTION_TYPES.S_PREP:
            _TargetProcessing.prep_ask_type(target_nouns, nl_question.question, raw_triple)
        elif nl_question.question_type == QUESTION_TYPES.HOW:
            _TargetProcessing.prep_how_type(target_nouns, nl_question.question, raw_triple)

        if nl_question.target in [QUESTION_TARGET.LOCATION, QUESTION_TARGET.TIME]:
            _TargetProcessing.loc_time_target(nl_question, target_nouns)
        else:
            for token in new_target_tokens:
                target_noun = NounEntity(token)

                if target_noun not in target_nouns:
                    if raw_triple.s.token == token:
                        if raw_triple.s not in target_nouns:
                            if raw_triple.s.is_var():
                                # E.g.: "Did Arnold Schwarzenegger attend a university?"
                                # dbr:Arnold_Schwarzenegger is NOT a var
                                target_nouns.append(raw_triple.s)
                    if raw_triple.o.token == token:
                        if raw_triple.o not in target_nouns:
                            # E.g.: "Give me all ESA astronauts.
                            if raw_triple.o.is_var():
                                target_nouns.append(raw_triple.o)

        if nl_question.target == QUESTION_TARGET.PERSON:
            _TargetProcessing.person_target(nl_question, target_nouns)


class _TargetProcessing:
    @staticmethod
    def loc_time_target(nl_question: NLQuestion, target_nouns: List[NounEntity]):
        # E.g.: "When did the Ming dynasty dissolve?"
        target_noun = NounEntity(nl_question.target)
    
        if target_noun not in target_nouns:
            target_nouns.append(target_noun)
    
    @staticmethod
    def person_target(nl_question: NLQuestion, target_nouns: List[NounEntity]):
        if len(target_nouns) == 0:
            # E.g.: "Who is the tallest basketball player?"
            target_noun = NounEntity(nl_question.target)
    
            if target_noun not in target_nouns:
                target_nouns.append(target_noun)
        else:
            # E.g.: "Who is the leader of the USA?"
            # Do nothing
            pass

    @staticmethod
    def prep_ask_type(target_nouns: List[NounEntity], sentence: Span, raw_triple: RawTriple):
        # E.g.: "In which country is Mecca located?"
        first_token = sentence[0]

        if raw_triple.s.token.head == first_token:
            target_nouns.append(raw_triple.s)

        if raw_triple.o.token.head == first_token:
            target_nouns.append(raw_triple.o)

    @staticmethod
    def prep_how_type(target_nouns: List[NounEntity], sentence: Span, raw_triple: RawTriple):
        # E.g.: "How high is the Yokohama Marine Tower?"
        root = sentence.root

        if raw_triple.s.token.head == root:
            target_nouns.append(raw_triple.o)


def _get_target_tokens(nl_question: NLQuestion, sentence: Span):
    target_nouns = []

    lefts = [token for token in list(sentence.root.lefts) if is_noun(token)]
    rights = [token for token in list(sentence.root.rights) if is_noun(token)]

    for token in sentence:
        if is_noun(token) and token.head == sentence.root:
            if nl_question.starts_with_wh(sentence) and len(lefts) > 0 and len(rights) > 0:
                # E.g.: "Which museum in New York has the most visitors?"
                if token in lefts:
                    target_nouns.append(token)
            else:
                target_nouns.append(token)

    return target_nouns
