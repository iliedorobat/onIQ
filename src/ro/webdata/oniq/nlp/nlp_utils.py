import warnings
from typing import Union
from spacy.tokens import Doc, Span, Token
from ro.webdata.oniq.common.constants import SYSTEM_MESSAGES


def get_cardinals(chunk):
    """
    Get the list of cardinals in a chunk

    :param chunk: The target chunk
    :return: The list of cardinals
    """
    return list([token for token in chunk if token.tag_ == "CD"])


def get_next_token(sentence: Span, aux_verb: Token, pos_list: [str]):
    """
    Get the next token which POS is not in pos_list

    :param sentence: The target sentence
    :param aux_verb: The auxiliary verb
    :param pos_list: The list of POS for which the iteration is allowed
    :return: The token after the auxiliary verb which POS not in pos_list
    """

    last_index = len(sentence) - 1
    next_index = aux_verb.i + 1

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


def get_prev_chunk(chunks: [Span], chunk: Span):
    warnings.warn(SYSTEM_MESSAGES.METHOD_NOT_USED, DeprecationWarning)

    chunk_index = chunks.index(chunk)
    if chunk_index > 0:
        return chunks[chunk_index - 1]
    return None


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
    return list([token for token in document if token.tag_ == 'WRB'])


def get_wh_determiner(document: Union[Doc, Span]):
    """
    Get the list of WH-determiners (tag = 'WDT'):\n
    - what, which, whose\n

    Resources:\n
    - https://grammar.collinsdictionary.com/easy-learning/wh-words\n
    - https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param document: The parsed document
    :return: The list of WH-determiners
    """
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
    return list([token for token in document if token.tag_ in ['WRB', 'WDT', 'WP', 'WP$']])


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

    first_word = phrase[0]
    return first_word.tag_ in ["WDT", "WP"] and first_word.dep_ == "nsubj"


def retokenize(document: Union[Doc, Span], sentence: Span):
    """
    Integrate the named entities into the document and retokenize it

    :param document: The parsed document
    :param sentence: The target sentence
    :return: Nothing
    """

    for named_entity in sentence.ents:
        with document.retokenize() as retokenizer:
            retokenizer.merge(named_entity)
