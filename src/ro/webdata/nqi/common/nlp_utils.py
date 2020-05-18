def get_wh_words(document):
    """
    Get the list of WH words\n
    https://www.ling.upenn.edu/hist-corpora/annotation/pos-wh.htm

    :param document:
    :return:
    """
    return list([token for token in document if token.tag_ == 'WDT'])


def retokenize(document, sentence):
    """
    Integrate the named entities into the document and retokenize it

    :param document:
    :param sentence:
    :return:
    """

    for named_entity in sentence.ents:
        with document.retokenize() as retokenizer:
            retokenizer.merge(named_entity)
