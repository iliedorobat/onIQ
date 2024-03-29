import json
import re
from typing import List, Union

import requests
from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.nlp_utils import text_to_span
from ro.webdata.oniq.common.nlp.utils import WordnetUtils, get_resource_namespace, get_resource_name
from ro.webdata.oniq.common.nlp.word_utils import get_prev_word, is_noun, is_adj_modifier
from ro.webdata.oniq.service.query_const import ACCESSORS, DATA_TYPE, PATHS
from ro.webdata.oniq.spacy_model import nlp_dbpedia
from ro.webdata.oniq.sparql.common.constants import SPARQL_VAR_PREFIX, SPARQL_STR_SEPARATOR


class NounEntity:
    def __init__(self, word: Union[str, Token], token: Token = None, is_dbpedia_type: bool = False):
        self.noun = None
        self.compound_noun = None
        self.is_dbpedia_type = is_dbpedia_type
        self.resource = None
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
                self.text = _prepare_text(self.compound_noun)
            elif is_adj_modifier(word):
                # E.g.: "Give me all Swedish holidays."

                self.compound_noun = _get_noun_entity(word)
                self.text = _prepare_text(self.compound_noun)
            else:
                self.compound_noun = _get_noun_entity(self.token)
                self.text = word.text

            self.resource = _get_resource(self.compound_noun, self.token)
        elif isinstance(word, Span):
            # E.g.: "Who is the author of the interpretation of dreams?"
            # E.g.: "how much is the total population of  european union?"
            self.compound_noun = word
            self.text = word.text
            self.resource = _get_resource(self.compound_noun, self.compound_noun)
        else:
            self.compound_noun = _get_noun_entity(self.token)
            self.text = word
            self.resource = _get_resource(self.compound_noun, self.token)

    def __eq__(self, other):
        if not isinstance(other, NounEntity):
            return NotImplemented
        return self.noun == other.noun

    def __hash__(self):
        return hash(self.text)

    def __str__(self):
        if self.is_dbpedia_type:
            if self.text is not None:
                # E.g.: "Give me all ESA astronauts."
                return self.text

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

    def is_res(self):
        # TODO: check if it contains ":"
        return "dbr:" in self.to_var()

    def is_text(self):
        return self.token is None

    def is_var(self):
        return SPARQL_VAR_PREFIX in self.to_var()

    def to_span(self):
        if self.compound_noun is None:
            return None

        first_noun = self.compound_noun[0]
        last_noun = self.compound_noun[len(self.compound_noun) - 1]
        prev_word = get_prev_word(first_noun)

        if self.noun is not None and is_adj_modifier(prev_word):
            # ADJ + compound noun
            # E.g.: "What is the net income of Apple?" => "net" + "income"
            # self.noun is None => "Give me all Swedish holidays."
            return Span(self.noun.doc, prev_word.i, last_noun.i + 1, label=self.compound_noun.root.ent_type)

        return self.compound_noun

    def to_var(self):
        if self.is_dbpedia_type:
            if self.text is not None:
                return self.text

        if self.resource is not None:
            return f"dbr:{self.resource[ACCESSORS.RESOURCE_NAME]}"

        if self.token is not None:
            text = re.sub(r"\s", SPARQL_STR_SEPARATOR, self.to_span().text)
            return f"{SPARQL_VAR_PREFIX}{text}"

        if self.text is not None:
            text = re.sub(r"\s", SPARQL_STR_SEPARATOR, self.text)
            return f"{SPARQL_VAR_PREFIX}{text}"

        return "NULL"


def _get_resource(compound_noun: Span, main_word: Token):
    if not isinstance(main_word, Span) and not _token_exists_in_ents(main_word):
        # E.g.: "Who is the youngest Pulitzer Prize winner?" => "winner"
        return None

    if is_adj_modifier(main_word):
        # E.g.: "Give me all Swedish holidays."
        country = WordnetUtils.find_country_by_nationality(main_word.text)
        country_span = text_to_span(country, 'GPE')

        query_params = [
            f'{ACCESSORS.QUESTION}={country_span.text}',
            f'{ACCESSORS.TARGET_DATA_TYPE}={DATA_TYPE.SPAN}',
            f'{ACCESSORS.START_I}={country_span.start}',
            f'{ACCESSORS.END_I}={country_span.end}'
        ]

        resource_uri = f'http://localhost:8200/{PATHS.ENTITIES}?{"&".join(query_params)}'
        resource_response = requests.get(resource_uri)

        return json.loads(resource_response.content)

    if _is_known_compound_named_entity(compound_noun):
        dbpedia_doc = nlp_dbpedia(compound_noun.doc)
        dbpedia_ents = [ent for ent in dbpedia_doc.ents if ent.start <= compound_noun.root.i <= ent.end]

        if len(dbpedia_ents) > 0:
            entity_span = dbpedia_ents[0]
            namespace = get_resource_namespace(entity_span)

            if entity_span.label_ == "DBPEDIA_ENT":
                # E.g.: "What is the net income of Apple?"
                return {
                    ACCESSORS.QUESTION: compound_noun.doc.text,
                    ACCESSORS.START_I: compound_noun.start,
                    ACCESSORS.END_I: compound_noun.end,
                    ACCESSORS.NAMED_ENTITY: entity_span.text,
                    ACCESSORS.RESOURCE_NAME: get_resource_name(entity_span),
                    ACCESSORS.RESOURCE_NAMESPACE: namespace
                }

        query_params = [
            f'{ACCESSORS.QUESTION}={compound_noun.doc.text}',
            f'{ACCESSORS.TARGET_DATA_TYPE}={DATA_TYPE.SPAN}',
            f'{ACCESSORS.START_I}={compound_noun.start}',
            f'{ACCESSORS.END_I}={compound_noun.end}'
        ]

        resource_uri = f'http://localhost:8200/{PATHS.ENTITIES}?{"&".join(query_params)}'
        resource_response = requests.get(resource_uri)

        return json.loads(resource_response.content)


def _token_exists_in_ents(token: Token):
    if not isinstance(token, Token):
        return False

    question = token.sent
    for ent in question.ents:
        if token in ent:
            # E.g.: "Who is the youngest Pulitzer Prize winner?"
            return True

    return False


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

    if noun.pos_ == "NOUN":
        # E.g.: Who is the person whose successor was Le Hong Phong? => "Phong".pos_ == "PROPN"
        if noun.dep_ == "attr":
            # E.g.: "Who is the youngest Pulitzer Prize winner?"
            return noun_list

    prev_word = get_prev_word(noun)

    if prev_word is None:
        # E.g.: "Desserts from which country contain fish?"
        return noun_list

    if is_noun(prev_word) and prev_word.dep_ == "compound":
        updated_noun_list = [prev_word] + noun_list

        return _get_compound_noun_parts(prev_word, updated_noun_list)
    elif prev_word.tag_ == "HYPH":
        # E.g.: "Who is the builder of Atamurat-Kerkichi Bridge ?"
        return _get_compound_noun_parts(prev_word, noun_list)

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
