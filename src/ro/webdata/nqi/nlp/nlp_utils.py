def get_verb_statements(document):
    verb_statements = []
    aux_verb = None
    negation = None
    wh_word = None

    for token in document:
        verb = token if token.pos_ in ["AUX", "VERB"] else None

        if verb is not None:
            if verb.pos_ == "AUX":
                aux_verb = verb
                negation = get_negation_token(document, aux_verb, negation)
                next_verb = get_next_verb(document, aux_verb)

                wh_word = get_wh_before_vb(document, token)
                if wh_word is None and verb.dep_ == "conj":
                    wh_word = verb_statements[len(verb_statements) - 1]["wh_word"]

                if next_verb is None or next_verb.pos_ != "VERB":
                    verb_statements.append({
                        "aux": aux_verb,
                        "neg": negation,
                        "verb": None,
                        "wh_word": wh_word
                    })
                    aux_verb = None
                    negation = None
                    wh_word = None
            else:
                if wh_word is None:
                    wh_word = get_wh_before_vb(document, token)
                    if wh_word is None and verb.dep_ == "conj":
                        wh_word = verb_statements[len(verb_statements) - 1]["wh_word"]

                negation = get_negation_token(document, verb, negation)
                verb_statements.append({
                    "aux": aux_verb,
                    "neg": negation,
                    "verb": verb,
                    "wh_word": wh_word
                })
                aux_verb = None
                negation = None
                wh_word = None

    return verb_statements


def get_next_verb(document, verb):
    next_word = document[verb.i + 1]

    # when was the museum opened
    # why are they always arrive late
    if next_word.pos_ == "DET":
        next_word = document[next_word.i + 1]

    if next_word.pos_ in ["NOUN", "PRON"]:
        next_word = document[next_word.i + 1]

    if next_word.pos_ in ["ADV"]:
        next_word = document[next_word.i + 1]

    if next_word.pos_ == "VERB":
        return next_word

    return None


def get_wh_before_vb(document, token):
    prev_word = document[token.i - 1]

    # E.g.: ... in museums which hosts ...
    if prev_word in get_wh_words(document):
        return prev_word

    # E.g.: where the famous artifacts are hosted?
    if prev_word.pos_ == "AUX":
        prev_word = document[prev_word.i - 1]

    if prev_word.pos_ in ["NOUN", "PRON"]:
        prev_word = document[prev_word.i - 1]

    if prev_word.pos_ in ["ADJ"]:
        prev_word = document[prev_word.i - 1]

    if prev_word.pos_ == "DET":
        prev_word = document[prev_word.i - 1]

    if prev_word in get_wh_words(document):
        return prev_word

    return None


def get_negation_token(document, verb, init_value):
    negation = init_value
    next_index = verb.i + 1

    if len(document) > next_index:
        next_word = document[next_index]
        negation = next_word if next_word.dep_ == "neg" else negation

    return negation


def get_verb_statements_bk(document):
    """
    Get the list of verb statements\n
    E.g.: "Give me museums which don't have artifacts"
    [
        {'aux': None, 'neg': None, 'verb': Give},
        {'aux': do, 'neg': n't, 'verb': have}
    ]

    :param document: The document
    :return: The list of verbs
    """

    verb_statements = []
    aux_verb = None
    negation = None

    for token in document:
        verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        verb = token if token.tag_ in verb_tags else None

        # [are, are, made]
        if verb is not None:
            prev_word = document[token.i - 1]
            wh_word = prev_word if prev_word in get_wh_words(document) else None

            if verb.pos_ == "AUX" or verb.dep_ in ["aux", "auxpass"]:
                aux_verb = verb
                negation = get_negation_token(document, aux_verb, negation)

                if document[aux_verb.i + 1].tag_ not in verb_tags:
                    verb_statements.append({
                        "aux": aux_verb,
                        "neg": negation,
                        "verb": None,
                        "wh_word": wh_word
                    })
                    aux_verb = None
                    negation = None
            else:
                negation = get_negation_token(document, verb, negation)
                verb_statements.append({
                    "aux": aux_verb,
                    "neg": negation,
                    "verb": verb,
                    "wh_word": wh_word
                })
                aux_verb = None
                negation = None

    return verb_statements


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
