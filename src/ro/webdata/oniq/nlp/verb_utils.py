from spacy.tokens import Span, Token

from ro.webdata.oniq.model.sentence.Verb import Verb
from ro.webdata.oniq.nlp.word_utils import is_aux_verb, is_verb


def get_verb_ancestor(chunk: Span):
    """
    Extract the first verb from the list of ancestors

    :param chunk: The current iterated chunk
    :return: The verb ancestor
    """

    if not isinstance(chunk, Span):
        return None

    ancestors = chunk.root.ancestors
    for token in ancestors:
        if is_verb(token):
            return token

    return None


def has_aux_verb(verb: Verb):
    if not isinstance(verb, Verb):
        return False

    verb_list = _prepare_verb_list(verb.aux_vbs, verb.main_vb)
    for token in verb_list:
        if is_aux_verb(token) and token.dep_ == "aux":
            return True

    return False


def _prepare_verb_list(aux_verbs, main_verb):
    verb_list = []

    if isinstance(main_verb, Token):
        verb_list.append(main_verb)

    if isinstance(aux_verbs, list):
        for token in aux_verbs:
            verb_list.append(token)

    return verb_list
