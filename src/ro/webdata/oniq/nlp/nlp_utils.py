import warnings
from typing import Union
from spacy.tokens import Doc, Span, Token

from ro.webdata.oniq.common.constants import SYSTEM_MESSAGES
from ro.webdata.oniq.common.print_const import COLORS
from ro.webdata.oniq.common.text_utils import MONTHS, array_exists_in_text, remove_determiner
from ro.webdata.oniq.nlp.utils import is_doc_or_span, is_empty_list
from ro.webdata.oniq.nlp.chunk_utils import get_first_word
from ro.webdata.oniq.nlp.word_utils import get_next_word, get_prev_word, is_adj, is_adv, is_verb, is_wh_word


def extract_chunk(chunk_list: [Span], word: Token):
    """
    Retrieve the chunk which contains the input token

    :param word: The token to be searched for
    :param chunk_list: The list of chunks (use case: "noun_chunks")
    :return: The identified chunk which contains the input token
    """

    if is_empty_list(chunk_list) or not isinstance(word, Token):
        return None

    # E.g.: "Where was the last place the picture was exposed?"
    if word.i == 0:
        return chunk_list[0]

    for chunk in chunk_list:
        for token in chunk:
            if word == token:
                return chunk

    return None


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


def get_noun_chunks(sentence: Union[Doc, Span]):
    """
    Get the list of noun chunks

    E.g.:
        - question: "Which is the noisiest and the largest city?"
        - chunks "Which", "the noisiest", "the largest city"

    :param sentence: The target sentence
    :return: The list of chunks
    """

    if not is_doc_or_span(sentence):
        return []

    chunk_list = _get_merged_noun_chunks(sentence)
    start_chunk = _get_start_chunk(sentence)
    first_word = get_first_word(start_chunk)

    # include the "which/how" chunk to the noun chunks list
    if is_wh_word(first_word):
        next_word = get_next_word(start_chunk[len(start_chunk) - 1])

        if is_verb(next_word):
            # E.g.: "How long does the museum remain closed?"
            if first_word.lower_ == "how" and next_word.dep_ != "ROOT":
                start_chunk = chunk_list[0]
                last_word = start_chunk[len(start_chunk) - 1]
                chunk_list[0] = sentence[0: last_word.i + 1]

            # E.g.: "How long is the journey?"
            else:
                chunk_list = [start_chunk] + chunk_list

        # E.g.: "Which is the noisiest and the largest city?"
        else:
            start_chunk = chunk_list[0]
            last_word = start_chunk[len(start_chunk) - 1]
            chunk_list[0] = sentence[0: last_word.i + 1]

    return _filter_chunk_list(sentence, chunk_list)


def _get_start_chunk(sentence: Union[Doc, Span]):
    if not is_doc_or_span(sentence) or len(sentence) == 0:
        return None

    # E.g.: "how old" / "how long"
    if sentence[0].lower_ == "how" and (is_adj(sentence[1]) or is_adv(sentence[1])):
        return sentence[0:2]

    return sentence[0:1]


def _get_merged_noun_chunks(sentence: Union[Doc, Span]):
    """
    Merge te chunks that are linked through a preposition and get the prepared list

    E.g.:
        - question: "Who is the director of Amsterdam museum?"
        - chunks: ["who", "the director", "Amsterdam museum"]
        - merged chunks: ["who", "the director of Amsterdam museum"]

    :param sentence: The target sentence
    :return: The list of chunks
    """

    # FIXME
    # E.g.: "The Goddess of Democracy, also known as the Goddess of Democracy and Freedom, the Spirit of Democracy,
    # and the Goddess of Liberty (自由女神; zìyóu nǚshén), was a 10-metre-tall (33 ft) statue created during the day
    # of April 10 Tiananmen Square protests"

    chunk_list = []
    original_chunk_list = list(sentence.noun_chunks)

    for index, chunk in enumerate(original_chunk_list):
        if index == 0:
            chunk_list.append(chunk)
        if index == len(original_chunk_list) - 1:
            break

        last_word = chunk[len(chunk) - 1]
        next_word = get_next_word(last_word)
        next_chunk = original_chunk_list[index + 1]

        # Merge two chunks that are linked through a preposition
        # E.g.: "Who is the director of Amsterdam museum?"
        # E.g.: "How many paintings are on display at the Amsterdam Museum?"
        # E.g.: "Where does the holder of the position of Lech Kaczynski live? [1]
        if next_word.dep_ == "prep":
            crr_chunk = chunk_list[len(chunk_list) - 1]
            chunk_list[len(chunk_list) - 1] = sentence[crr_chunk.start: next_chunk.end]
        else:
            chunk_list.append(next_chunk)

    return chunk_list


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

    if not is_doc_or_span(sentence) or is_empty_list(chunk_list):
        return filtered_list

    for index, chunk in enumerate(chunk_list):
        if len(chunk) == 1:
            if index == 0 or chunk[0] not in get_wh_words(sentence):
                filtered_list.append(chunk)
        else:
            filtered_list.append(chunk)

    return filtered_list


def get_chunk_index(chunk_list: [Span], chunk: Span):
    """
    Retrieve the chunk's position in chunk_list

    :param chunk_list: The list of chunks (use case: "noun_chunks")
    :param chunk: The target chunk
    :return: The index of the target chunk
    """

    if is_empty_list(chunk_list) or not isinstance(chunk, Span):
        return -1

    for index, item in enumerate(chunk_list):
        if item == chunk:
            return index

    return -1


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


def get_prev_chunk(chunks: [Span], chunk: Span):
    warnings.warn(SYSTEM_MESSAGES.METHOD_NOT_USED, DeprecationWarning)

    if is_empty_list(chunks) or not isinstance(chunk, Span):
        return None

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

    if not is_doc_or_span(document):
        return []

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
    print(f'{COLORS.LIGHT_RED} Do not use retokenizer with Spacy v3!')

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
