from typing import List

from spacy.tokens import Token, Span

from ro.webdata.oniq.common.nlp.word_utils import is_noun
from ro.webdata.oniq.sparql.NLQuestion import NLQuestion, QUESTION_TYPES
from ro.webdata.oniq.sparql.NounEntity import NounEntity
from ro.webdata.oniq.sparql.triples.Triple import Triple


class Targets:
    def __init__(self, nl_question: NLQuestion, triples: List[Triple]):
        self.values = init_targets(nl_question, triples)


def init_targets(nl_question: NLQuestion, triples: List[Triple]):
    targets = []

    for raw_triple in triples:
        _update_targets(nl_question, targets, raw_triple)

    return list(set(targets))


def _update_targets(nl_question: NLQuestion, target_nouns: List[NounEntity], triple: Triple):
    new_target_tokens = _init_target_tokens(nl_question, nl_question.question)

    # ORDER IS CRUCIAL
    if nl_question.question_type == QUESTION_TYPES.S_PREP:
        _TargetProcessing.prep_ask_type(nl_question, triple, target_nouns)
    elif nl_question.question_type == QUESTION_TYPES.HOW:
        _TargetProcessing.prep_how_type(nl_question, triple, target_nouns)

    for token in new_target_tokens:
        target_noun = NounEntity(token)

        if target_noun not in target_nouns:
            if triple.s.token == token:
                if triple.s not in target_nouns:
                    if triple.s.is_var():
                        # E.g.: "Did Arnold Schwarzenegger attend a university?"
                        # dbr:Arnold_Schwarzenegger is NOT a var
                        target_nouns.append(triple.s)
            if triple.o.token == token:
                if triple.o not in target_nouns:
                    if triple.o.is_var():
                        # E.g.: "Did Arnold Schwarzenegger attend a university?"
                        # => ?university is var
                        target_nouns.append(triple.o)
            if triple.s.is_text():
                if triple.s.is_var():
                    if target_noun.token.text == triple.s.text:
                        # E.g.: "Give me all ESA astronauts."
                        target_nouns.append(triple.s)
            if triple.o.is_text():
                if triple.o.is_var():
                    # E.g.: "When did the Ming dynasty dissolve?"
                    target_nouns.append(triple.o)


def _init_target_tokens(nl_question: NLQuestion, sentence: Span):
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


class _TargetProcessing:
    @staticmethod
    def prep_ask_type(nl_question: NLQuestion, triple: Triple, target_nouns: List[NounEntity]):
        # E.g.: "In which country is Mecca located?"
        first_token = nl_question.question[0]
        s_token = triple.s.token
        o_token = triple.o.token

        if isinstance(s_token, Token) and s_token.head == first_token:
            if triple.s.is_var():
                target_nouns.append(triple.s)

        if isinstance(o_token, Token) and o_token.head == first_token:
            if triple.o.is_var():
                # E.g.: "In which country is Mecca located?" => not isinstance(o_token, Token)
                target_nouns.append(triple.o)

    @staticmethod
    def prep_how_type(nl_question: NLQuestion, triple: Triple, target_nouns: List[NounEntity]):
        # E.g.: "How high is the Yokohama Marine Tower?"
        root = nl_question.question.root

        if triple.s.token.head == root:
            target_nouns.append(triple.o)
