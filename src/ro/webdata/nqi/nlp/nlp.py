def get_verbs(document):
    """
    Get the list of verbs\n

    :param document: The document
    :return: The list of verbs
    """
    return list([token for token in document if token.tag_ in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']])


def get_wh_adverbs(document):
    """
    Get the list of WH-adverbs:\n
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
    Get the list of WH-determiners:\n
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
    Get the list of WH-pronouns\n
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
