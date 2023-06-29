from typing import List

from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.word_utils import is_noun
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, QUESTION_TYPES, ANSWER_TYPE
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class RawTargetUtils:
    @staticmethod
    def update_targets(nl_question: NLQuestion, target_nouns: List[NounEntity], raw_triple: RawTriple):
        new_target_tokens = _get_target_tokens(nl_question, nl_question.question)

        # ORDER IS CRUCIAL
        if nl_question.question_type == QUESTION_TYPES.S_PREP:
            _TargetProcessing.prep_ask_type(nl_question, raw_triple, target_nouns)
        elif nl_question.question_type == QUESTION_TYPES.HOW:
            _TargetProcessing.prep_how_type(nl_question, raw_triple, target_nouns)

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
                        if raw_triple.o.is_var():
                            # E.g.: "Did Arnold Schwarzenegger attend a university?"
                            # => ?university is var
                            target_nouns.append(raw_triple.o)
                if raw_triple.s.is_text():
                    if raw_triple.s.is_var():
                        if target_noun.token.text == raw_triple.s.text:
                            # E.g.: "Give me all ESA astronauts."
                            target_nouns.append(raw_triple.s)
                if raw_triple.o.is_text():
                    if raw_triple.o.is_var():
                        # E.g.: "When did the Ming dynasty dissolve?"
                        target_nouns.append(raw_triple.o)


class _TargetProcessing:
    @staticmethod
    def prep_ask_type(nl_question: NLQuestion, raw_triple: RawTriple, target_nouns: List[NounEntity]):
        # E.g.: "In which country is Mecca located?"
        first_token = nl_question.question[0]
        s_token = raw_triple.s.token
        o_token = raw_triple.o.token

        if isinstance(s_token, Token) and s_token.head == first_token:
            if raw_triple.s.is_var():
                target_nouns.append(raw_triple.s)

        if isinstance(o_token, Token) and o_token.head == first_token:
            if raw_triple.o.is_var():
                # E.g.: "In which country is Mecca located?" => not isinstance(o_token, Token)
                target_nouns.append(raw_triple.o)

    @staticmethod
    def prep_how_type(nl_question: NLQuestion, raw_triple: RawTriple, target_nouns: List[NounEntity]):
        # E.g.: "How high is the Yokohama Marine Tower?"
        root = nl_question.question.root

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
