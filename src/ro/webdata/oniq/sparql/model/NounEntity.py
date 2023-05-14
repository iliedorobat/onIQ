import re
from typing import List, Union

from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.nlp_utils import token_to_span
from ro.webdata.oniq.common.nlp.utils import WordnetUtils
from ro.webdata.oniq.common.nlp.word_utils import get_prev_word, is_noun, is_adj_modifier

VARNAME_SEPARATOR = "_"


class NounEntity:
    def __init__(self, word: Union[str, Token], token: Token = None, is_dbpedia_type: bool = False):
        self.noun = None
        self.compound_noun = None
        self.is_named_entity = False
        self.is_text = True
        self.is_dbpedia_type = is_dbpedia_type
        self.text = None
        self.token = None

        if isinstance(token, Token):
            # E.g.: "Who is the tallest basketball player?"
            # E.g.: "Give me all ESA astronauts."
            self.token = token
        elif isinstance(word, Token):
            self.token = word

        if isinstance(word, Token):
            if is_noun(word):
                self.noun = word
                self.compound_noun = _get_noun_entity(word)
                self.is_named_entity = _is_known_named_entity(word) or _is_known_compound_named_entity(self.compound_noun)
                self.is_text = False
                self.text = _prepare_text(self.compound_noun)
            elif is_adj_modifier(word):
                # E.g.: "Give me all Swedish holidays."

                self.compound_noun = _get_noun_entity(word)
                self.is_named_entity = _is_known_named_entity(word) or _is_known_compound_named_entity(self.compound_noun)
                self.is_text = True
                self.text = WordnetUtils.find_country_by_nationality(word.text)
        else:
            self.text = word

    def __eq__(self, other):
        if not isinstance(other, NounEntity):
            return NotImplemented
        return self.noun == other.noun

    def __str__(self):
        if self.compound_noun is not None:
            return self.compound_noun.text
        elif self.noun is not None:
            return self.to_span()
        elif self.text is not None:
            return self.text
        else:
            return "NULL"

    @staticmethod
    def get_noun_entity(noun: Token):
        return _get_noun_entity(noun)

    def is_null(self):
        return str(self) == "NULL"

    def is_var(self):
        return "?" in self.to_var()

    def to_span(self):
        compound_noun = _get_noun_entity(self.noun)
        first_noun = compound_noun[0]
        last_noun = compound_noun[len(compound_noun) - 1]
        prev_word = get_prev_word(first_noun)

        if is_adj_modifier(prev_word):
            # ADJ + compound noun
            return Span(self.noun.doc, prev_word.i, last_noun.i + 1, label=compound_noun.root.ent_type)

        return token_to_span(self.noun)

    def to_var(self):
        if isinstance(self.compound_noun, Span):
            if self.is_named_entity:
                text = self.compound_noun.text
                if self.is_text:
                    # E.g.: "Give me all Swedish holidays."
                    text = self.text

                # FIXME: workaround => lookup for "Public company"
                is_org = self.compound_noun.root.ent_type_ == "ORG" and text.lower().__contains__("apple")
                if is_org:
                    # E.g.: "What is the net income of Apple?"
                    text += "_Inc."
                return "res:" + re.sub(r"\s", VARNAME_SEPARATOR, text)

        if self.noun is not None:
            text = re.sub(r"\s", VARNAME_SEPARATOR, self.to_span().text)
            return f"?{text}"

        if self.text is not None:
            if self.is_dbpedia_type:
                return self.text

            text = re.sub(r"\s", VARNAME_SEPARATOR, self.text)
            return f"?{text}"

        return "NULL"


def _is_known_compound_named_entity(compound_noun: Span):
    if compound_noun is None:
        return False
    
    for noun in compound_noun:
        if _is_known_named_entity(noun) is True:
            return True
    
    return False


def _is_known_named_entity(noun: Token):
    if not isinstance(noun, Token):
        return False

    target_noun = noun

    if noun.dep_ == "attr":
        # E.g.: "Who is the youngest Pulitzer Prize winner?"
        target_noun = get_prev_word(noun)

    for named_entity in target_noun.doc.ents:
        if named_entity.start <= target_noun.i < named_entity.end:
            return True

    return False


def _get_noun_entity(noun):
    """
    Join together two or more nouns which make up a noun_entity.

    E.g.:
        - question: "What did James Cagney win in the 15th Academy Awards?":
            * target noun = "Cagney".
            * noun_entity = "James Cagney".
            * type = compound.
        - question: "What ice cream flavor does Will Smith like?":
            * target noun = "flavor".
            * noun_entity = "ice cream flavor".
            * type = compound.
        - question: "How many artifacts does the museum host?":
            * target noun = "artifacts".
            * noun_entity = "artifacts".
            * type = simple.

    Args:
        noun (Token): Target noun.

    Returns:
        Span: Noun entity.
    """

    if not isinstance(noun, Token):
        return None

    noun_list = _get_compound_noun_parts(noun, [noun])
    # FIXME: brother in law
    is_simple_noun = len(noun_list) == 1  # the noun_entity consists of a single noun

    if is_simple_noun:
        return Span(noun.doc, noun.i, noun.i + 1, label=noun.ent_type)

    noun_list = [
        noun for noun in noun_list
        if (noun.pos_ == "NOUN" and noun.dep_ != "attr")  # E.g.: "Who is the youngest Pulitzer Prize winner?"
        or noun.pos_ != "NOUN"  # E.g.: "Whose successor is Le Hong Phong?"
    ]
    first_noun = noun_list[0]
    last_noun = noun_list[len(noun_list) - 1]

    return Span(noun.doc, first_noun.i, last_noun.i + 1, label=noun.ent_type)


def _get_compound_noun_parts(noun, noun_list):
    """
    Retrieve the list of nouns that are part of a noun_entity.

    E.g.:
        - question: "What did James Cagney win in the 15th Academy Awards?":
            * noun_entity = "James Cagney".

    Args:
        noun (Token): Target noun.
        noun_list (List[Token]): Initial list of noun_parts.

    Returns:
        List[Token]: List of nouns that are part of a noun_entity.
    """

    prev_word = get_prev_word(noun)

    if is_noun(prev_word) and prev_word.dep_ == "compound":
        updated_noun_list = [prev_word] + noun_list

        return _get_compound_noun_parts(prev_word, updated_noun_list)

    return noun_list


def _prepare_text(compound_noun: Span):
    text = ""

    for index, token in enumerate(compound_noun):
        if index > 0:
            text += " "

        # transform the plural form to singular
        # E.g.: "soccer players" => "soccer player"
        if token.tag_ in ["NNS", "NNPS"]:
            text += token.lemma_
        else:
            text += token.text

    if text == "":
        return None

    return text