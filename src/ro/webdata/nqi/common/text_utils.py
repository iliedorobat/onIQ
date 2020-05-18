import re


def split_camel_case_string(value):
    """
    Split a camel-case string into multiple lower case pieces.
    E.g.:
        * wasPresentAt => was present at;
        * WasPresentAt => was present at.
    """
    # https://www.geeksforgeeks.org/python-split-camelcase-string-to-individual-strings/
    arr = re.findall(r'[a-zA-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', value)
    arr = [item.lower() for item in arr]
    separator = " "
    return separator.join(arr)
