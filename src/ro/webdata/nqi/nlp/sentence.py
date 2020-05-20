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


def get_type(document, sentence, has_main_sentence):
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
    :param has_main_sentence: A flag which specifies if the main sentence has been already detected
    :return: The type of the sentence
    """

    wh_words = get_wh_words(document)
    root = sentence.root

    if root in wh_words:
        return "wh_start"
    else:
        if has_main_sentence is False and root.tag_[0:2] == "NN":
            return "main"
        else:
            return "secondary"


def get_verb(sentence, verb_list):
    """
    TODO: update the documentation
    Get the verb in a sentence

    :param sentence: The sentence
    :param verb_list: The list of verbs
    :return: The verb
    """

    index_range = range(0, len(verb_list))

    for index in reversed(index_range):
        verb_item = verb_list[index]

        if verb_item["is_available"] is True and sentence.start > verb_item["token"].i:
            verb_list[index]["is_available"] = False
            return verb_list[index]["token"]
