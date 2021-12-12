import warnings
from typing import Union
from spacy.tokens import Doc, Span, Token

from ro.webdata.oniq.common.constants import SYSTEM_MESSAGES
from ro.webdata.oniq.common.print_const import COLORS
from ro.webdata.oniq.common.text_utils import MONTHS, array_exists_in_text, remove_determiner
from ro.webdata.oniq.nlp.utils import is_doc_or_span
from ro.webdata.oniq.nlp.word_utils import get_prev_word, is_wh_word


def get_cardinals(sentence: Span):
    """
    Get the list of cardinals in a chunk

    :param sentence: The target sentence
    :return: The list of cardinals
    """

    warnings.warn(SYSTEM_MESSAGES.METHOD_NOT_USED, DeprecationWarning)

    if not isinstance(sentence, Span):
        return []

    return list([token for token in sentence if token.tag_ == "CD"])


def get_next_token(word: Token, pos_list: [str]):
    """
    Get the next token which POS is not in pos_list

    :param word: The target token
    :param pos_list: The list of POS for which the iteration is allowed
    :return: The token after the target token which POS not in pos_list
    """

    if not isinstance(word, Token) or not isinstance(pos_list, list):
        return None

    sentence = word.sent
    last_index = len(sentence) - 1
    next_index = word.i + 1

    if next_index > last_index:
        return None

    if next_index == last_index:
        return sentence[next_index]

    next_word = sentence[next_index]

    for i in range(next_index, last_index):
        token = sentence[i]

        # E.g.: token.dep_ != 'attr' => "Which is the noisiest and the largest city?"
        # TODO: token.pos_ == "PUNCT"; e.g.: "Where are the coins, pictures and swords located?"
        if (token.pos_ in pos_list or token.dep_ == "neg") and token.dep_ != "attr":
            next_word = sentence[token.i + 1]
        else:
            break

    return next_word


def get_wh_adverbs(document: Union[Doc, Span]):
    """
    Get the list of WH-adverbs (tag = 'WRB'):\n
    - when, where, why\n
    - whence, whereby, wherein, whereupon\n
    - how\n

    Resources:\n
    - https://grammar.collinsdictionary.com/easy-learning/wh-words\n
    - https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param document: The parsed document
    :return: The list of WH-adverbs
    """

    if not is_doc_or_span(document):
        return []

    return list([token for token in document if token.tag_ == 'WRB'])


def get_wh_determiners(document: Union[Doc, Span]):
    """
    Get the list of WH-determiners (tag = 'WDT'):\n
    - what, which, whose\n

    Resources:\n
    - https://grammar.collinsdictionary.com/easy-learning/wh-words\n
    - https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param document: The parsed document
    :return: The list of WH-determiners
    """

    if not is_doc_or_span(document):
        return []

    return list([token for token in document if token.tag_ == 'WDT'])


def get_wh_pronouns(document: Union[Doc, Span]):
    """
    Get the list of WH-pronouns (tag in ['WP', 'WP$'])\n
    - who, whose, which, what\n

    Resources:\n
    - https://grammar.collinsdictionary.com/easy-learning/wh-words\n
    - https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param document: The parsed document
    :return: The list of WH-pronouns
    """

    if not is_doc_or_span(document):
        return []

    return list([token for token in document if token.tag_ in ['WP', 'WP$']])


def get_wh_words(document: Union[Doc, Span]):
    """
    Get the list of WH-words\n
    - when, where, why\n
    - whence, whereby, wherein, whereupon\n
    - how\n
    - what, which, whose\n
    - who, whose, which, what\n

    Resources:\n
    - https://grammar.collinsdictionary.com/easy-learning/wh-words\n
    - https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param document: The parsed document
    :return: The list of WH-words
    """

    if not is_doc_or_span(document):
        return []

    return list([token for token in document if token.tag_ in ['WDT', 'WP', 'WP$', 'WRB']])


# TODO: ilie.dorobat: add the documentation
def is_wh_noun_chunk(chunk: Span):
    if not isinstance(chunk, Span) or len(chunk) > 1:
        return False

    return is_wh_word(chunk[0])


def is_wh_noun_phrase(phrase: Union[Doc, Span]):
    """
    Determine if the phrase is a WH-noun phrase

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - Wh-noun phrase: "Which"

    E.g.:
        - question: "Who is the most beautiful woman?"
        - Wh-noun phrase: "Who"

    :param phrase: The target phrase/chunk/document
    :return: True/False
    """

    warnings.warn(SYSTEM_MESSAGES.METHOD_NOT_USED, DeprecationWarning)

    if not is_doc_or_span(phrase):
        return []

    first_word = phrase[0]
    return first_word.tag_ in ["WDT", "WP"] and first_word.dep_ == "nsubj"


def retokenize(document: Union[Doc, Span], sentence: Span):
    """
    Integrate the named entities into the document and retokenize it

    :param document: The parsed document
    :param sentence: The target sentence
    :return: Nothing
    """

    warnings.warn(SYSTEM_MESSAGES.METHOD_USED_WITH_SPACY_2, DeprecationWarning)

    for named_entity in sentence.ents:
        raw_entity = _prepare_compound_entity(named_entity)
        entity = remove_determiner(raw_entity)
        with document.retokenize() as retokenizer:
            # E.g.: "Was the statue created during the day of April 10 Tiananmen Square protests?"
            if not array_exists_in_text(MONTHS, entity.text.lower()):
                retokenizer.merge(entity)


def _prepare_compound_entity(named_entity: Span):
    """
    Join two or more words which have a "compound" dependency

    E.g.:
        - "Where is adam mickiewicz monument?"
        - named_entity: "adam mickiewicz monument"
        - compound_entity: "adam mickiewicz"

    :param named_entity: The initial named entity
    :return: The compound named_entity
    """

    if not isinstance(named_entity, Span):
        return None

    start_i = -1
    end_i = -1

    for word in named_entity:
        if word.dep_ == "compound":
            if start_i == -1:
                start_i = _get_start_i(word)
            end_i = word.i

    if start_i > -1:
        return named_entity.sent[start_i: end_i + 1]

    return named_entity


def _get_start_i(word: Token):
    if not isinstance(word, Token):
        return -1

    prev_word = get_prev_word(word)
    if not isinstance(prev_word, Token):
        return -1

    # E.g.: "Where can one find farhad and shirin monument?" (spacy v2)
    if prev_word.pos_ == "CCONJ":
        prev_word = get_prev_word(prev_word)
        return _get_start_i(prev_word)

    return word.i
