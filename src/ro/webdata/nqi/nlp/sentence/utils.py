def get_cardinals(chunk):
    """
    Get the list of cardinals in a chunk

    :param chunk: The chunk
    :return: The list of cardinals
    """
    return list([token for token in chunk if token.tag_ == "CD"])


def get_conjunction(document, chunks, chunk_index):
    # TODO: pos_ == "PUNCT" => comma: "which is the museum which hosts more than 10 pictures, one sword?"
    chunk = chunks[chunk_index]
    prev_chunk = chunks[chunk_index - 1] if chunk_index > 0 else None
    # The index of the last token of the previous chunk
    prev_chunk_last_index = prev_chunk[len(prev_chunk) - 1].i if prev_chunk is not None else 0

    for i in reversed(range(chunk[0].i + 1)):
        prev_token_index = i - 1

        if prev_token_index > prev_chunk_last_index:
            prev_token = document[prev_token_index]

            if prev_token.pos_ == "CCONJ" and prev_token.tag_ == "CC":
                return prev_token

    return None


def get_preposition(sentence, chunk):
    first_index = chunk[0].i
    prev_word = sentence[first_index - 1] if first_index > 0 else None

    if prev_word is not None and prev_word.dep_ == "prep":
        return prev_word

    return None


def get_prev_chunk(chunks, chunk_index):
    if chunk_index > 0:
        return chunks[chunk_index - 1]
    return None


def get_wh_adverbs(document):
    """
    Get the list of WH-adverbs (tag = 'WRB'):\n
    - when, where, why\n
    - whence, whereby, wherein, whereupon\n
    - how\n

    Resources:\n
    - https://grammar.collinsdictionary.com/easy-learning/wh-words\n
    - https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param document: The document
    :return: The list of WH-adverbs
    """
    return list([token for token in document if token.tag_ == 'WRB'])


def get_wh_determiner(document):
    """
    Get the list of WH-determiners (tag = 'WDT'):\n
    - what, which, whose\n

    Resources:\n
    - https://grammar.collinsdictionary.com/easy-learning/wh-words\n
    - https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param document: The document
    :return: The list of WH-determiners
    """
    return list([token for token in document if token.tag_ == 'WDT'])


def get_wh_pronouns(document):
    """
    Get the list of WH-pronouns (tag in ['WP', 'WP$'])\n
    - who, whose, which, what\n

    Resources:\n
    - https://grammar.collinsdictionary.com/easy-learning/wh-words\n
    - https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param document: The document
    :return: The list of WH-pronouns
    """
    return list([token for token in document if token.tag_ in ['WP', 'WP$']])


def get_wh_words(document):
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

    :param document: The document
    :return: The list of WH-words
    """
    return list([token for token in document if token.tag_ in ['WRB', 'WDT', 'WP', 'WP$']])


def retokenize(document, sentence):
    """
    Integrate the named entities into the document and retokenize it

    :param document: The document
    :param sentence: The sentence
    :return: Nothing
    """

    for named_entity in sentence.ents:
        with document.retokenize() as retokenizer:
            retokenizer.merge(named_entity)
