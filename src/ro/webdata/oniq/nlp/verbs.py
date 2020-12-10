from spacy.tokens import Span, Token
from ro.webdata.oniq.model.sentence.Verb import Verb
from ro.webdata.oniq.nlp.nlp_utils import get_wh_words


# TODO: prepare_action_list => build the actions here
# TODO: move the negation and the adjective inside of the actions
def prepare_verb_list(sentence: Span):
    verb_statements = []
    aux_verb = modal_verb = negation = None
    verb_list = _get_verb_list(sentence)

    for verb in verb_list:
        if isinstance(verb, list):
            aux_verb = verb
            next_verb = _get_main_verb(sentence, aux_verb[len(aux_verb) - 1])
            negation = _get_negation(sentence, aux_verb[0], negation)
            adj_list = _get_adj_list(sentence, aux_verb[len(aux_verb) - 1])

            if next_verb is None:
                # Adding a neutral value ("None") in order to assure the loop iteration
                if len(adj_list) == 0:
                    adj_list.append(None)

                for adjective in adj_list:
                    verb = Verb(aux_verb, negation, None, modal_verb, adjective)
                    verb_statements.append(verb)

                aux_verb = modal_verb = negation = None
        elif isinstance(verb, Token):
            if verb.tag_ == "MD":
                modal_verb = verb
            else:
                negation = _get_negation(sentence, verb, negation)
                verb = Verb(aux_verb, negation, verb, modal_verb, None)
                verb_statements.append(verb)
                aux_verb = modal_verb = negation = None

    return verb_statements


def _get_verb_list(sentence: Span):
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


def _is_aux_preceded_by_aux(sentence: Span, verb: Token):
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


def _get_main_verb(sentence: Span, aux_verb: Token):
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

    next_word = _get_next_token(sentence, aux_verb, ["DET", "ADV", "ADJ", "CCONJ", "NOUN", "PRON", "PROPN"])

    if next_word is not None and next_word.pos_ == "VERB":
        # E.g.: "Who is the director who own 10 cars and sold a house or a panel?"
        if sentence[next_word.i - 1] not in get_wh_words(sentence):
            return next_word

    return None


# TODO: extracting long adjectives: "most beautiful"
def _get_adj_list(sentence: Span, aux_verb: Token):
    """
    Get the list of adjectives

    :param sentence: The target sentence
    :param aux_verb: The auxiliary verb
    :return: The list of adjectives
    """

    next_word = _get_next_token(sentence, aux_verb, ["DET", "ADV", "CCONJ", "NOUN", "PRON", "PROPN", "VERB"])
    next_words = []

    if next_word is not None:
        # E.g.: "is married"
        if next_word.pos_ == "ADJ" or (next_word.pos_ == "NOUN" and next_word.dep_ == "attr"):
            next_words.append(next_word)

        # Example of question which has two adjectives => "Which is the noisiest and the largest city?"
        next_word = _get_next_token(sentence, next_word, ["DET", "ADV", "NOUN", "PRON", "PROPN", "VERB"])
        if next_word.pos_ == "CCONJ":
            next_words = next_words + _get_adj_list(sentence, next_word)

    return next_words


def _get_next_token(sentence: Span, aux_verb: Token, pos_list: [str]):
    """
    Get the next token which POS is not in pos_list

    :param sentence: The target sentence
    :param aux_verb: The auxiliary verb
    :param pos_list: The list of POS for which the iteration is allowed
    :return: The token after the auxiliary verb which POS not in pos_list
    """

    last_index = len(sentence) - 1
    next_index = aux_verb.i + 1

    if next_index > last_index:
        return None

    if next_index == last_index:
        return sentence[next_index]

    next_word = sentence[next_index]

    for i in range(next_index, last_index):
        token = sentence[i]

        # E.g.: token.dep_ != 'attr' => "Which is the noisiest and the largest city?"
        if (token.pos_ in pos_list or token.dep_ == "neg") and token.dep_ != "attr":
            next_word = sentence[token.i + 1]
        else:
            break

    return next_word


def _get_negation(sentence: Span, verb: Token, init_negation: Token):
    """
    Get the negation

    :param sentence: The target sentence
    :param verb: Main verb, auxiliary verb or modal verb
    :param init_negation: The initial value of the negation
    :return: The identified negation
    """

    negation = init_negation
    next_index = verb.i + 1

    if next_index < len(sentence):
        next_word = sentence[next_index]
        negation = next_word if next_word.dep_ == "neg" else negation

    return negation
