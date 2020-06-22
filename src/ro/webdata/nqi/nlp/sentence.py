import numpy

from ro.webdata.nqi.nlp.Action import Action
from ro.webdata.nqi.nlp.nlp_utils import get_verb_statements


PRONOUNS = [
    "i", "me",
    "you", "thee",
    "he", "him",
    "she", "her",
    "it",
    "we", "us",
    "they", "them",
    "its"
]


SENTENCE_TYPE = {
    "SELECT_CLAUSE": "select clause",
    "WHERE_CLAUSE": "where clause",

    "PRONOUN": "pronoun sentence",
    "WH_PRONOUN_START": "WH Pronoun start sentence",
    "WH_START": "WH start sentence"
}


def get_cardinals(chunk):
    """
    Get the list of cardinals in a chunk

    :param chunk: The chunk
    :return: The list of cardinals
    """
    return list([token for token in chunk if token.tag_ == "CD"])


def get_nouns(chunk, *dependencies: []):
    """
    Get the list of nouns in a sentence

    :param dependencies: The list of dependencies used for filtering
    :param chunk: The sentence
    :return: The list of nouns
    """

    nouns = []

    for token in chunk:
        if token.tag_[0:2] == "NN" and (
                len(dependencies) == 0 or token.dep_ in numpy.asarray(dependencies)
        ):
            nouns.append({
                "dependency": token.dep_,
                "is_root": token.text == chunk.root.text,
                "value": token
            })

    return nouns


def get_preposition(sentence, chunk):
    first_index = chunk[0].i
    prev_word = sentence[first_index - 1] if first_index > 0 else None

    if prev_word is not None and prev_word.dep_ == "prep":
        return prev_word

    return None


def get_action(sentence, chunks, chunk_index, actions, statements, stmt_type):
    if stmt_type not in [SENTENCE_TYPE["PRONOUN"], SENTENCE_TYPE["WH_START"], SENTENCE_TYPE["WH_PRONOUN_START"]]:
        chunk = chunks[chunk_index]
        conj_nouns = get_nouns(chunk, ["conj"])
        last_action = statements[len(statements) - 1].action if len(statements) > 0 else {}

        first_word = sentence[0]
        prev_word = sentence[chunk.start - 1] if chunk.start > 0 else None

        for action in actions:
            if prev_word is not None and prev_word.tag_ != "IN":
                # WP: who are your friends which own a car?
                # WP: what is the name of the biggest museum which hosts 10 pictures?
                # WRB: where the artifacts are located in museums which hosts more than 10 artifacts?
                if first_word.tag_ in ["WP", "WRB"]:
                    if action.is_available is True:
                        action.is_available = False
                        return action
                    if len(conj_nouns) > 0:
                        return last_action


def get_actions(sentence):
    actions = []
    verb_statements = get_verb_statements(sentence)

    for verb_stmt in verb_statements:
        dep = verb_stmt.main_vb.dep_ \
            if verb_stmt.main_vb is not None \
            else verb_stmt.aux_vb.dep_
        actions.append(Action(dep, verb_stmt))

    return actions


def get_prev_chunk(chunks, chunk_index):
    if chunk_index > 0:
        return chunks[chunk_index - 1]
    return None
