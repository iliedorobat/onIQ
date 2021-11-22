from typing import Union
from spacy.tokens import Doc, Span


def is_doc_or_span(sentence: Union[Doc, Span]):
    return isinstance(sentence, Doc) or isinstance(sentence, Span)


def is_empty_list(input_list: list):
    return not isinstance(input_list, list) or len(input_list) == 0
