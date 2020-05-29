from ro.webdata.nqi.common.constants import PRONOUNS, SENTENCE_TYPE
from ro.webdata.nqi.nlp.nlp import get_wh_words


def get_cardinals(sentence):
    """
    Get the list of cardinals in a sentence

    :param sentence: The sentence
    :return: The list of cardinals
    """

    cardinals = []

    for token in sentence:
        if token.tag_ == "CD":
            cardinals.append(token)

    return cardinals


def get_nouns(sentence):
    """
    Get the list of nouns in a sentence

    :param sentence: The sentence
    :return: The list of nouns
    """

    nouns = []

    for token in sentence:
        if token.tag_[0:2] == "NN":
            nouns.append({
                "dependency": token.dep_,
                "is_root": token.text == sentence.root.text,
                "value": token
            })

    return nouns


def get_type(document, sentence):
    """
    Get the type of sentence:\n
    - wh_start: the fist sentence if the query starts with a WH-word
    - main: the sentence after the wh_start, or the first one
    - secondary: any other sentences

    "Which are the most visited museums which exposed at least 10 artifacts":\n
    - sent 1: "Which"
    - sent 2: "the most visited museums"
    - sent 3: "at least 10 artifacts"

    :param document: The document
    :param sentence: The sentence
    :return: The type of the sentence
    """

    if sentence.text.lower() in PRONOUNS:
        return SENTENCE_TYPE["PRONOUN"]
    elif sentence.root in get_wh_words(document):
        return SENTENCE_TYPE["WH_START"]
    elif is_main_sentence(document, sentence) is True:
        return SENTENCE_TYPE["MAIN"]
    else:
        return SENTENCE_TYPE["SECONDARY"]


def is_main_sentence(document, sentence):
    """
    TODO: documentation
    """

    # Get the list of wh determiners excepting the first one which is used for asking
    wh_determiners = [token for token in get_wh_words(document) if token.i > 0]
    determiners = list(
        filter(
            lambda token: token.i < sentence.start, wh_determiners
        )
    )

    return len(determiners) == 0


def get_action(document, sentence, verb_list):
    """
    TODO: documentation
    Get the verb in a sentence
    """

    index_range = range(0, len(verb_list))

    for index in reversed(index_range):
        verb = verb_list[index]

        if sentence.start > verb["token"].i:
            if is_main_sentence(document, sentence) is True:
                verb["is_available"] = False
                verb["is_main"] = True
                return verb["token"]
            else:
                if verb["is_main"] is False and verb["is_available"] is True:
                    verb["is_available"] = False
                    return verb["token"]
