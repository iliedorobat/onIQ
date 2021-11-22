from spacy.tokens import Span
from ro.webdata.oniq.nlp.word_utils import is_verb


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
