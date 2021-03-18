from spacy.tokens import Span, Token
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Adjective import Adjective
from ro.webdata.oniq.model.sentence.Verb import Verb, get_main_verb, is_aux_preceded_by_aux
from ro.webdata.oniq.nlp.nlp_utils import get_next_token, is_wh_word


def get_action_list(sentence: Span):
    action_list = []
    aux_verbs = modal_verb = None
    verb_list = _get_verb_list(sentence)

    for verb_item in verb_list:
        if isinstance(verb_item, list):
            aux_verbs = verb_item
            next_verb = get_main_verb(sentence, aux_verbs[len(aux_verbs) - 1])
            adj_list = _get_adj_list(sentence, aux_verbs[len(aux_verbs) - 1])
            acomp_list = [adjective for adjective in adj_list if adjective.adj.dep_ == "acomp"]

            if next_verb is None:
                # Add a neutral value ("None") in order to assure the loop iteration
                if len(acomp_list) == 0:
                    acomp_list.append(None)

                for acomp in acomp_list:
                    verb = Verb(aux_verbs, None, modal_verb, acomp)
                    action = Action(sentence, verb)
                    action_list.append(action)

                aux_verbs = modal_verb = None
        elif isinstance(verb_item, Token):
            if verb_item.tag_ == "MD":
                modal_verb = verb_item
            else:
                # E.g.: "What is the federated state located in the Weimar Republic?" [1]
                # "is" and "located" should be part of different Actions
                if _is_prev_wh_word(sentence, aux_verbs):
                    verb = Verb(aux_verbs, None, modal_verb, None)
                    action = Action(sentence, verb)
                    action_list.append(action)
                    aux_verbs = None

                verb = Verb(aux_verbs, verb_item, modal_verb, None)
                action = Action(sentence, verb)
                action_list.append(action)

                aux_verbs = modal_verb = None

    return action_list


def _is_prev_wh_word(sentence: Span, aux_verbs: list):
    """
    Check whether or not the word before the first auxiliary verb is a wh_word

    :param sentence: The target sentence
    :param aux_verbs: The list of auxiliary verbs
    :return: True/False
    """

    if aux_verbs is None or len(aux_verbs) == 0:
        return False

    first_index = aux_verbs[0].i
    if first_index == 0:
        return False

    prev_word = sentence[first_index - 1]
    return is_wh_word(prev_word)


def _get_verb_list(sentence: Span):
    """
    Prepare the list of verbs as follows:
        - the auxiliary verbs are stored as a list of tokens,
        - the main verb is stored as a single token

    E.g.:
        TODO: a better example
        sentence: "have not been displayed" => return [[has, been], displayed]

    :param sentence: The target sentence
    :return: The list of verbs
    """

    verb_list = []

    for token in sentence:
        verb = token if token.pos_ in ["AUX", "VERB"] else None

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


def _get_adj_list(sentence: Span, aux_verb: Token):
    """
    Get the list of adjectives

    :param sentence: The target sentence
    :param aux_verb: The auxiliary verb
    :return: The list of adjectives
    """

    next_word = get_next_token(sentence, aux_verb, ["DET", "ADV", "CCONJ", "NOUN", "PRON", "PROPN", "VERB"])
    adj_list = []

    if next_word is not None:
        #                              E.g.: "is married"
        if next_word.pos_ == "ADJ" or (next_word.pos_ == "NOUN" and next_word.dep_ == "attr"):
            adj = Adjective(sentence, next_word)
            adj_list.append(adj)

        # Example of question which has two adjectives => "Which is the noisiest and the largest city?"
        next_word = get_next_token(sentence, next_word, ["DET", "ADV", "NOUN", "PRON", "PROPN", "VERB"])

        # E.g.: "Who is the most beautiful woman and the most generous person?"
        if next_word is not None and next_word.pos_ == "NOUN" and next_word.dep_ == "attr":
            next_word = get_next_token(sentence, next_word, ["DET", "ADV", "NOUN", "PRON", "PROPN", "VERB"])

        if next_word is not None and next_word.pos_ == "CCONJ":
            adj_list = adj_list + _get_adj_list(sentence, next_word)

    return adj_list
