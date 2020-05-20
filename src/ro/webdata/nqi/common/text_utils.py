import re


def split_camel_case_string(value, separator=" "):
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
