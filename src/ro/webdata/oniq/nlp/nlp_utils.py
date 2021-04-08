import warnings
from typing import Union
from spacy.tokens import Doc, Span, Token
from ro.webdata.oniq.common.constants import SYSTEM_MESSAGES
from ro.webdata.oniq.nlp.word_utils import is_noun, is_nsubj_wh_word, is_verb, is_wh_word


def get_cardinals(sentence: Span):
    """
    Get the list of cardinals in a chunk

    :param sentence: The target sentence
    :return: The list of cardinals
    """
    return list([token for token in sentence if token.tag_ == "CD"])


def get_chunk(chunk_list: [Span], word: Token):
    """
    Retrieve the chunk which contains the input token

    :param word: The token to be searched for
    :param chunk_list: The list of chunks (use case: "noun_chunks")
    :return: The identified chunk which contains the input token
    """

    # E.g.: "Where was the last place the picture was exposed?"
    if word.i == 0:
        return chunk_list[0]

    for chunk in chunk_list:
        for token in chunk:
            if word == token:
                return chunk
    return None


def get_noun_chunks(sentence: Union[Doc, Span]):
    """
    Get the list of noun chunks

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"

    :param sentence: The target sentence
    :return: The list of chunks
    """

    chunk_list = list(sentence.noun_chunks)
    first_chunk = sentence[0:1] if len(sentence) > 0 else None
    first_word = first_chunk[0] if len(first_chunk) > 0 else None

    # include the "which" chunk to the noun chunks list
    # E.g.: "Which is the noisiest and the largest city?"
    if is_nsubj_wh_word(sentence, first_word):
        chunk_list = [first_chunk] + chunk_list
    # E.g.: "Which beautiful female is married to a writer born in Rome and has three children?"
    elif is_wh_word(first_word):
        first_chunk = chunk_list[0]
        last_word = first_chunk[len(first_chunk) - 1]
        chunk_list[0] = sentence[0: last_word.i + 1]

    return _filter_chunk_list(sentence, chunk_list)


def _filter_chunk_list(sentence: Union[Doc, Span], chunk_list: [Span]):
    """
    Exclude the WH-words chunks-like from the list of chunks, excepting for the first entry

    E.g.: "Who is the director who own 2 cars and sold a house or a panel?"
        - chunk_list = ["Who", "the director", "who", "10 cars", "a house", "a panel"]
        - WH-words chunks-like: [chunk_list[2]]
        - filtered_list = ["Who", "the director", "10 cars", "a house", "a panel"]

    :param sentence: The target sentence
    :param chunk_list: The target list of chunks
    :return: The filtered list of chunks
    """

    filtered_list = []

    for index, chunk in enumerate(chunk_list):
        if len(chunk) == 1:
            if index == 0 or chunk[0] not in get_wh_words(sentence):
                filtered_list.append(chunk)
        else:
            filtered_list.append(chunk)

    return filtered_list


def get_chunk_index(chunk_list: [Span], chunk: Span):
    """
    Retrieve the chunk's index from chunk_list

    :param chunk_list: The list of chunks (use case: "noun_chunks")
    :param chunk: The target chunk
    :return: The index of the target chunk
    """

    for index, item in enumerate(chunk_list):
        if item == chunk:
            return index
    return -1


def get_noun_ancestor(chunk: Span):
    """
    Extract the first NOUN / PROPN from the list of ancestors

    :param chunk: The current iterated chunk
    :return: The noun ancestor
    """

    ancestors = chunk.root.ancestors
    for token in ancestors:
        if is_noun(token):
            return token
    return None


def get_verb_ancestor(chunk: Span):
    """
    Extract the first verb from the list of ancestors

    :param chunk: The current iterated chunk
    :return: The verb ancestor
    """

    ancestors = chunk.root.ancestors
    for token in ancestors:
        if is_verb(token):
            return token
    return None


def get_next_token(sentence: Span, word: Token, pos_list: [str]):
    """
    Get the next token which POS is not in pos_list

    :param sentence: The target sentence
    :param word: The target token
    :param pos_list: The list of POS for which the iteration is allowed
    :return: The token after the target token which POS not in pos_list
    """

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
    return list([token for token in document if token.tag_ in ['WDT', 'WP', 'WP$', 'WRB']])


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
