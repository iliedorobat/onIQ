from spacy.tokens import Span, Token
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Adjective import Adjective
from ro.webdata.oniq.model.sentence.Verb import Verb, get_main_verb, is_aux_preceded_by_aux
from ro.webdata.oniq.nlp.nlp_utils import get_next_token
from ro.webdata.oniq.nlp.word_utils import is_conjunction, is_verb, is_wh_word


def get_action_list(sentence: Span):
    action_list = []
    aux_verbs = modal_verb = None
    verb_list = _get_verb_list(sentence)

    for verb_item in verb_list:
        if isinstance(verb_item, list):
            aux_verbs = verb_item
            next_verb = get_main_verb(sentence, aux_verbs[len(aux_verbs) - 1])
            adj_list = _get_adj_list(sentence, aux_verbs[len(aux_verbs) - 1], [])
            acomp_list = _generate_acomp_list(adj_list)

            # E.g.: dep_ == "acomp" => "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?"
            # E.g.: dep_ == "ROOT" => "When was Bibi Andersson married to Per Ahlmark?" [1]
            if next_verb is None or len(acomp_list) > 0:
                verb = Verb(aux_verbs, None, modal_verb)
                action = Action(sentence, verb, acomp_list)
                action_list.append(action)

                aux_verbs = modal_verb = None
        elif isinstance(verb_item, Token):
            if verb_item.tag_ == "MD":
                modal_verb = verb_item
            else:
                # FIXME
                # # E.g.: "When did Lena Horne receive the Grammy Award for Best Jazz Vocal Album?" [1]
                # # "is" and "located" should be part of different Actions
                # if _is_prev_wh_word(sentence, aux_verbs):
                #     verb = Verb(aux_verbs, None, modal_verb)
                #     action = Action(sentence, verb, None)
                #     action_list.append(action)
                #     aux_verbs = None

                # E.g.: "How long does the museum remain closed?"
                adj_list = _get_adj_list(sentence, verb_item, [])
                acomp_list = _generate_acomp_list(adj_list)

                verb = Verb(aux_verbs, verb_item, modal_verb)
                action = Action(sentence, verb, acomp_list)
                action_list.append(action)

                aux_verbs = modal_verb = None

    return action_list


def is_part_of_action(action_list: [Action], word: Token):
    """
    Determine if the input word is part of an entry in the action_list

    :param action_list: The list of events (Actions)
    :param word: The target token
    :return: True/False
    """

    for action in action_list:
        token_list = action.verb.to_list()
        if action.acomp_list is not None:
            for acomp in action.acomp_list:
                token_list.append(acomp.token)

        for token in token_list:
            if token == word:
                return True

    return False


def _generate_acomp_list(adj_list: [Adjective]):
    # TODO: amod: "Which woman is beautiful, generous, tall and pretty?"
    # TODO: remove filter?
    acomp_list = [
        adjective for adjective in adj_list
        # E.g.: "Which woman is beautiful, generous, tall and sweet?"
        if adjective.token.dep_ in ["acomp", "conj", "intj", "ROOT"]
    ]

    for acomp in acomp_list:
        for conj_token in acomp.token.conjuncts:
            adj = _get_adj(adj_list, conj_token)
            if adj is not None and _get_adj(acomp_list, adj.token) is None:
                acomp_list.append(adj)

    return acomp_list


def _get_adj(adj_list: [Adjective], word: Token):
    for adj in adj_list:
        if adj.token == word:
            return adj
    return None


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

    next_word = get_next_token(sentence, aux_verb, ["DET", "ADV", "CCONJ", "NOUN", "PRON", "PROPN", "VERB"])

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

        if next_word is not None and is_conjunction(next_word):
            return _get_adj_list(sentence, next_word, adj_list)

    return adj_list
