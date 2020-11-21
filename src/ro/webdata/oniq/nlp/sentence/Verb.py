from ro.webdata.oniq.nlp.sentence.utils import get_wh_words
from spacy.tokens import Token


class Verb:
    def __init__(self, aux_vb, neg, main_vb, modal_vb, wh_word):
        self.aux_vb = aux_vb
        self.neg = neg
        self.main_vb = main_vb
        self.modal_vb = modal_vb
        self.wh_word = wh_word

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        aux_vb = self.aux_vb if self else None
        neg = self.neg if self else None
        main_vb = self.main_vb if self else None
        modal_vb = self.modal_vb if self else None
        wh_word = self.wh_word if self else None

        return (
            f'{{'
            f'\n{indentation}\taux_vb: {aux_vb},'
            f'\n{indentation}\tneg: {neg},'
            f'\n{indentation}\tmain_vb: {main_vb},'
            f'\n{indentation}\tmodal_vb: {modal_vb},'
            f'\n{indentation}\twh_word: {wh_word}'
            f'\n{indentation}}}'
        )


def get_verb(verb_stmt):
    if verb_stmt.main_vb is not None:
        return verb_stmt.main_vb
    return verb_stmt.aux_vb


def prepare_verb_list(sentence):
    verb_statements = []
    aux_verb = modal_verb = negation = wh_word = None
    verb_list = _get_verb_list(sentence)

    for verb in verb_list:
        if isinstance(verb, list):
            aux_verb = verb
            next_verb = _get_main_verb(sentence, aux_verb[len(aux_verb) - 1])
            negation = _get_negation_token(sentence, aux_verb[0], negation)
            wh_word = _get_wh_before_vb(sentence, aux_verb[0])
            wh_word = _get_prev_wh_word(wh_word, verb_statements, aux_verb)

            if next_verb is None:
                verb_statements.append(
                    Verb(aux_verb, negation, None, modal_verb, wh_word)
                )
                aux_verb = modal_verb = negation = wh_word = None
        elif isinstance(verb, Token):
            if wh_word is None:
                wh_word = _get_wh_before_vb(sentence, verb)
                wh_word = _get_prev_wh_word(wh_word, verb_statements, [verb])

            if verb.tag_ == "MD":
                modal_verb = verb
            else:
                negation = _get_negation_token(sentence, verb, negation)
                verb_statements.append(
                    Verb(aux_verb, negation, verb, modal_verb, wh_word)
                )
                aux_verb = modal_verb = negation = wh_word = None

    return verb_statements


def _get_prev_wh_word(wh_word, verb_statements, verb_list):
    # TODO: check the conj_list
    conj_list = list(
        filter(
            lambda item: item.dep_ == "conj", verb_list
        )
    )

    # TODO: check the statement
    if wh_word is None and len(conj_list) > 0:
        return verb_statements[len(verb_statements) - 1].wh_word

    return wh_word


def _get_verb_list(sentence):
    """
    Prepare the list of verbs as follows:
        - the auxiliary verbs are stored as a list of tokens,
        - the main verb is stored as a single token

    E.g.:
        TODO: a better example
        sentence: "have not been displayed" => return [[has, been], displayed]

    :param sentence:
    :return:
    """

    verb_list = []

    for token in sentence:
        verb = token if token.pos_ in ["AUX", "VERB"] else None

        if verb is not None:
            if _is_aux_preceded_by_aux(sentence, verb):
                length = len(verb_list)
                verb_list[length - 1].append(verb)
            else:
                if verb.pos_ == "AUX":
                    verb_list.append([verb])
                else:
                    verb_list.append(verb)

    return verb_list


def _is_aux_preceded_by_aux(sentence, verb):
    """
    Check if the auxiliary verb is preceded by another auxiliary verb

    E.g.:
        question: "which statues do not have more than three owners?"
            * aux ("have") preceded by aux ("do"): "do not have"

    :param sentence: The sentence
    :param verb: The auxiliary verb
    :return:
    """

    if verb.pos_ != "AUX" or verb.i == 0:
        return False

    prev_word = sentence[verb.i - 1]

    if prev_word.dep_ == "neg" and verb.i > 1:
        prev_word = sentence[verb.i - 2]

    if prev_word.pos_ == "AUX":
        return True

    return False


def _get_main_verb(sentence, verb):
    """
    Get the main verb

    E.g.:
        question: "when was the museum opened?"
            * the verb chain: "was opened" => return "opened"
        question: "why do they always arrive late?"
            * the verb chain: "do arrive" => return "arrive"
        question: "when were the panama papers published"
            * the verb chain: "were published" => return "published"

    :param sentence: The sentence
    :param verb: The auxiliary verb
    :return: The main verb or None
    """

    next_word = _get_next_token(sentence, verb, ["DET", "ADV", "ADJ", "CCONJ", "NOUN", "PRON", "PROPN"])

    if next_word is not None and next_word.pos_ == "VERB":
        # who is the director who own 10 cars and sold a house or a panel?
        if sentence[next_word.i - 1] not in get_wh_words(sentence):
            return next_word

    return None


def _get_next_token(document, verb, pos_list):
    if verb.i + 1 >= len(document):
        return None

    next_word = document[verb.i + 1]

    for i in range(next_word.i, len(document)):
        token = document[i]

        if token.pos_ in pos_list or token.dep_ == "neg":
            next_word = document[token.i + 1]
        else:
            break

    return next_word


def _get_wh_before_vb(document, token):
    fragment = _get_prev_fragment(document[0: token.i + 1], ["AUX"])
    fragment = _get_prev_fragment(fragment, ["ADJ", "ADV", "NOUN", "PRON"])

    if fragment is not None and len(fragment) == 1 and fragment[0] in get_wh_words(document):
        return fragment[0]
    return None


def _get_prev_fragment(document, main_pos_list):
    if document is None:
        return None
    if len(document) == 1:
        return document[0: 1]

    # [...] and [...] one of the [...]
    #      CCONJ      NUM ADP DET
    pos_list = main_pos_list + ["ADP", "CCONJ", "DET", "NUM", "PUNCT"]
    prev_token = None
    wh_words = get_wh_words(document)

    for i in reversed(range(len(document))):
        token = document[i]
        if i == 0 or token in wh_words:
            return document[token.i: token.i + 1]
        elif token.pos_ not in pos_list:
            return document[0: i + 1]
        prev_token = document[i - 1]

    return document[0: prev_token.i + 1]


def _get_negation_token(document, verb, init_value):
    negation = init_value
    next_index = verb.i + 1

    if len(document) > next_index:
        next_word = document[next_index]
        negation = next_word if next_word.dep_ == "neg" else negation

    return negation
