import warnings
from spacy.tokens import Span, Token
from ro.webdata.oniq.common.constants import SYSTEM_MESSAGES
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Adjective import Adjective
from ro.webdata.oniq.model.sentence.Verb import Verb, get_main_verb, is_aux_preceded_by_aux
from ro.webdata.oniq.nlp.nlp_utils import get_next_token
from ro.webdata.oniq.nlp.utils import is_empty_list
from ro.webdata.oniq.nlp.word_utils import get_next_word, is_adj, is_conjunction, is_verb, is_wh_word


# TODO: ilie.dorobat: "Where can one find farhad and shirin monument?" => check the action list
# TODO: ilie.dorobat: add the documentation
def get_action_list(sentence: Span):
    action_list = []

    if not isinstance(sentence, Span):
        return action_list

    aux_verbs = modal_verb = None
    verb_list = _get_verb_list(sentence)

    for verb_item in verb_list:
        if isinstance(verb_item, list):
            aux_verbs = verb_item
            next_verb = get_main_verb(aux_verbs[len(aux_verbs) - 1])
            is_followed_by_adj = _is_followed_by_adj(aux_verbs)

            # E.g.: "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?"
            # E.g.: "When was Bibi Andersson married to Per Ahlmark?" [1]
            if is_followed_by_adj or next_verb is None:
                verb = Verb(aux_verbs, None, modal_verb)
                action = Action(sentence, verb)
                action_list.append(action)

                aux_verbs = modal_verb = None
        elif isinstance(verb_item, Token):
            if verb_item.tag_ == "MD":
                modal_verb = verb_item
            else:
                # FIXME: "When did Lena Horne receive the Grammy Award for Best Jazz Vocal Album?" [1]

                verb = Verb(aux_verbs, verb_item, modal_verb)
                action = Action(sentence, verb)
                action_list.append(action)

                aux_verbs = modal_verb = None

    return action_list


def _is_followed_by_adj(aux_verbs: [Verb]):
    """
    Check if the aux verbs are followed by an adjective

    E.g.:
        - query: "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?"
            - verb: "is"
            - adj: "married"
        - query: "When was Bibi Andersson married to Per Ahlmark?" [1]
            - verb: "was"
            - adj: "married"

    :param aux_verbs: The list of aux verbs
    :return: True/False
    """

    if not isinstance(aux_verbs, list) or len(aux_verbs) == 0:
        return False

    last_aux = aux_verbs[len(aux_verbs) - 1]
    next_word = get_next_word(last_aux)

    if not isinstance(next_word, Token):
        return False

    # E.g.: "When was Bibi Andersson married to Per Ahlmark?"
    while next_word.pos_ == "PROPN":
        next_word = get_next_word(next_word)

    if is_adj(next_word):
        return True


def is_part_of_action(action_list: [Action], word: Token):
    """
    Determine if the input word is part of an entry in the action_list

    :param action_list: The list of events (Actions)
    :param word: The target token
    :return: True/False
    """

    if is_empty_list(action_list) or not isinstance(word, Token):
        return False

    for action in action_list:
        token_list = action.verb.to_list()
        if action.acomp_list is not None:
            for acomp in action.acomp_list:
                token_list.append(acomp.token)

        for token in token_list:
            if token == word:
                return True

    return False


def _get_verb_list(sentence: Span):
    """
    Prepare the list of verbs as follows:
        - the auxiliary verbs are stored as a list of tokens,
        - the main verb is stored as a single token

    E.g.:
        - query: "Which paintings and statues have not been deposited in Bacau"
            - returned value: [[have, been], deposited]

    :param sentence: The target sentence
    :return: The list of verbs
    """

    verb_list = []

    if not isinstance(sentence, Span):
        return verb_list

    for token in sentence:
        verb = token if is_verb(token) else None

        if verb is not None:
            if is_aux_preceded_by_aux(sentence, verb):
                length = len(verb_list)
                verb_list[length - 1].append(verb)
            else:
                if verb.pos_ == "AUX":
                    verb_list.append([verb])
                else:
                    verb_list.append(verb)

    return verb_list


def _get_adj_list(sentence: Span, aux_verb: Token, adj_list: [Adjective]):
    """
    Get the list of adjectives

    :param sentence: The target sentence
    :param aux_verb: The auxiliary verb
    :return: The list of adjectives
    """

    warnings.warn(SYSTEM_MESSAGES.METHOD_NOT_USED, DeprecationWarning)

    if not isinstance(adj_list, list) \
            or not isinstance(sentence, Span) \
            or not isinstance(aux_verb, Token):
        return []

    next_word = get_next_token(aux_verb, ["DET", "ADV", "CCONJ", "NOUN", "PRON", "PROPN", "VERB"])

    if next_word is not None:
        if is_adj(next_word):
            adj = Adjective(next_word)
            adj_list.append(adj)

        # Example of question which has two adjectives => "Which is the noisiest and the largest city?"
        next_word = get_next_token(next_word, ["DET", "ADV", "NOUN", "PRON", "PROPN", "VERB"])

        # E.g.: "Who is the most beautiful woman and the most generous person?"
        if next_word is not None and next_word.pos_ == "NOUN" and next_word.dep_ == "attr":
            next_word = get_next_token(next_word, ["DET", "ADV", "NOUN", "PRON", "PROPN", "VERB"])

        if next_word is not None and is_conjunction(next_word):
            return _get_adj_list(sentence, next_word, adj_list)

    return adj_list
