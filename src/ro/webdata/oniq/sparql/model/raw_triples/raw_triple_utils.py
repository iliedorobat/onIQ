from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.sentence_utils import contains_multiple_wh_words, ends_with_verb
from ro.webdata.oniq.common.nlp.word_utils import is_noun, is_aux, is_verb


def get_related_verb(word: Token, sentence: Span):
    """
    Get the word whose head is the input word.

    :param word: The target head.
    :param sentence: The target sentence.
    :return: Token.
    """

    for token in sentence:
        if is_verb(token) and token.head == word:
            return token

    return None


def get_child_noun(word: Token, span: Span):
    for token in span:
        if token.i > word.i and token.pos_ == "ADP":
            # E.g.: "Who is the leader of the town where the Myntdu river originates?"
            return get_child_noun(token, token.sent[token.i + 1:])

        # "Where was the designer of REP Parasol born?"
        is_auxpass = is_aux(token.head) and token.head.head == word

        if token.head == word or is_auxpass:
            if token.dep_ == "auxpass":
                if contains_multiple_wh_words(word.sent):
                    if ends_with_verb(span):
                        # E.g.: ### "Where was the person who won the oscar born?"
                        return get_child_noun(token, token.sent[token.i + 1:])
                    else:
                        # E.g.: "Where was the person born whose successor was Le Hong Phong?"
                        pass
                else:
                    # E.g.: "Where is Fort Knox located?"
                    pass  # nothing to do

            if is_noun(token) and token.dep_ != "conj":
                # E.g.: token.dep_ != "conj" => "What is the population and area of the most populated state?"
                return token

            if token.pos_ == "NUM":
                # E.g.: "who is the one who baptized Ion's father?"
                return token

    return None
