from spacy.tokens import Token


# TODO: documentation
class Noun:
    def __init__(self, dep: str, is_root: bool, value: Token):
        self.dep = dep
        self.is_root = is_root
        self.value = value
