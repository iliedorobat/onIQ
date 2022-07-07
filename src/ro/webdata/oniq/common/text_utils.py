import re
from spacy.tokens import Span


MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

WORD_SEPARATOR = " "


# TODO: doc
# TODO: text.lower()
def array_exists_in_text(array, text):
    for item in array:
        if item.lower() in text:
            return True
    return False


def remove_determiner(sentence: Span):
    """
    TODO: ilie.dorobat: move the method to chunk_utils?
    Remove the determiner from the passed sentence\n
    It is used to clean name entities.
    E.g.:
        - question: "Where is the Museum of Amsterdam?"
        - named entities: ["the Museum of Amsterdam"]
        - prepared named entities: ["Museum of Amsterdam"]

    :param sentence: The sentence
    :return: The prepared sentence
    """

    if not isinstance(sentence, Span):
        return sentence

    first_word = sentence[0]

    if first_word.pos_ == "DET":
        return sentence[1: len(sentence)]

    return sentence


def split_camel_case_string(value, separator=WORD_SEPARATOR):
    """
    Split a camel-case string into multiple lower case pieces.\n
    E.g.:
        - wasPresentAt => was present at
        - WasPresentAt => was present at

    Resources:
        - https://www.geeksforgeeks.org/python-split-camelcase-string-to-individual-strings/

    :param value: The input string
    :param separator: The string separator
    :return: The formatted string
    """

    arr = re.findall(r'[a-zA-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', value)
    arr = [item.lower() for item in arr]

    return separator.join(arr)
