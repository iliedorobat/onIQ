from spacy.tokens import Token


# TODO: documentation
class Noun:
    def __init__(self, dep: str, is_root: bool, value: Token):
        self.dep = dep
        self.is_root = is_root
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Noun):
            return NotImplemented
        return other is not None and \
            self.dep == other.dep and \
            self.is_root == other.is_root and \
            self.value == other.value
