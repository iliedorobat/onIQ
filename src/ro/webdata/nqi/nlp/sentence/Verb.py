from ro.webdata.nqi.nlp.sentence.utils import get_wh_words


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
            f'{indentation}{{ '
            f'{indentation}aux_vb: {aux_vb}, '
            f'{indentation}neg: {neg}, '
            f'{indentation}main_vb: {main_vb}, '
            f'{indentation}modal_vb: {modal_vb}, '
            f'{indentation}wh_word: {wh_word} '
            f'{indentation}}}'
        )


def get_verb_statements(sentence):
    verb_statements = []
    aux_verb = modal_verb = negation = wh_word = None

    for token in sentence:
        verb = token if token.pos_ in ["AUX", "VERB"] else None

        if verb is not None:
            if verb.pos_ == "AUX":
                aux_verb = verb
                next_verb = _get_main_verb(sentence, aux_verb)
                wh_word = _get_wh_before_vb(sentence, token)

                if wh_word is None and verb.dep_ == "conj":
                    wh_word = verb_statements[len(verb_statements) - 1].wh_word

                # TODO: OLD condition: if next_verb is None or next_verb.pos_ != "VERB":
                print('aux_verb, next_verb', aux_verb, next_verb)
                if next_verb is None:
                    negation = _get_negation_token(sentence, aux_verb, negation)
                    verb_statements.append(
                        Verb(aux_verb, negation, None, modal_verb, wh_word)
                    )
                    aux_verb = modal_verb = negation = wh_word = None
            else:
                if wh_word is None:
                    wh_word = _get_wh_before_vb(sentence, token)

                    if wh_word is None and verb.dep_ == "conj":
                        wh_word = verb_statements[len(verb_statements) - 1].wh_word

                if verb.tag_ == "MD":
                    modal_verb = verb
                else:
                    negation = _get_negation_token(sentence, verb, negation)
                    verb_statements.append(
                        Verb(aux_verb, negation, verb, modal_verb, wh_word)
                    )
                    aux_verb = modal_verb = negation = wh_word = None

    return verb_statements


def _get_main_verb(sentence, verb):
    """
    Get the main verb

    E.g.:\n
    - question: "when was the museum opened?"
        * the verb chain: "was opened" => return "opened"
    - question: "why do they always arrive late?"
        * the verb chain: "do arrive" => return "arrive"
    - question: "when were the panama papers published"
        * the verb chain: "were published" => return "published"

    :param sentence: The sentence
    :param verb: The auxiliary verb
    :return: The main verb or None
    """

    next_word = _get_next_token(sentence, verb, ["DET", "ADV", "ADJ", "NOUN", "PRON", "PROPN"])

    if next_word.pos_ == "VERB":
        # who is the director who own 10 cars and sold a house or a panel?
        if sentence[next_word.i - 1] not in get_wh_words(sentence):
            return next_word

    return None


def _get_next_token(document, verb, pos_list):
    next_word = document[verb.i + 1]

    for i in range(next_word.i, len(document)):
        token = document[i]

        if token.pos_ in pos_list:
            next_word = document[token.i + 1]
        else:
            break

    return next_word


def _get_wh_before_vb(document, token):
    prev_word = document[token.i - 1]

    # E.g.: ... in museums which hosts ...
    if prev_word in get_wh_words(document):
        return prev_word

    # E.g.: where the famous artifacts are hosted?
    if prev_word.pos_ == "AUX":
        prev_word = document[prev_word.i - 1]

    if prev_word.pos_ in ["NOUN", "PRON"]:
        prev_word = document[prev_word.i - 1]

    if prev_word.pos_ in ["ADJ"]:
        prev_word = document[prev_word.i - 1]

    if prev_word.pos_ == "DET":
        prev_word = document[prev_word.i - 1]

    if prev_word in get_wh_words(document):
        return prev_word

    return None


def _get_negation_token(document, verb, init_value):
    negation = init_value
    next_index = verb.i + 1

    if len(document) > next_index:
        next_word = document[next_index]
        negation = next_word if next_word.dep_ == "neg" else negation

    return negation
