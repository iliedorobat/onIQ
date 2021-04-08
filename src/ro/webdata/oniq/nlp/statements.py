from spacy.tokens import Doc, Span, Token
from iteration_utilities import unique_everseen

from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Phrase import Phrase
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.nlp.actions import get_action_list, is_part_of_action
from ro.webdata.oniq.nlp.nlp_utils import get_cardinals, get_chunk, get_noun_ancestor, get_noun_chunks, \
    get_verb_ancestor, is_wh_noun_phrase, retokenize
from ro.webdata.oniq.nlp.phrase import prepare_phrase_list
from ro.webdata.oniq.nlp.word_utils import is_nsubj_wh_word, is_verb


def get_statement_list(document: Doc):
    """
    Get the list of statements generated around the target phrases

    :param document: The parsed document
    :return: A list of statements
    """
    statements = []

    for sentence in document.sents:
        retokenize(document, sentence)
        action_list = get_action_list(sentence)
        statements = _generate_statement_list(sentence, action_list)

        echo.token_list(sentence)
        echo.action_list(action_list)
        echo.statement_list(statements)

    return statements


def _generate_statement_list(sentence, action_list):
    statements = []

    # TODO: phrase_list = prepare_phrase_list(sentence) => instead of get_noun_chunks ???
    chunk_list = get_noun_chunks(sentence)
    # Filter the chunks which are not in dependence of conjunction because they will be added
    # to target_chunks or related_chunks through the _get_associated_chunks method
    filtered_chunks = list(filter(lambda item: item.root.dep_ != "conj", chunk_list))

    for chunk in filtered_chunks:
        main_ancestor = _get_main_ancestor(chunk)
        main_chunk = get_chunk(filtered_chunks, main_ancestor)

        # E.g.: "Which paintings and statues have not been deposited in Bacau?"
        if main_chunk != chunk:
            target_chunks = _get_associated_chunks(chunk_list, main_chunk)
            related_chunks = _get_associated_chunks(chunk_list, chunk)

            for target_chunk in target_chunks:
                for related_chunk in related_chunks:
                    if target_chunk != related_chunk:
                        verb = get_verb_ancestor(related_chunk)
                        action = _get_action(action_list, verb)

                        # if action is not None and action.acomp_list is not None:
                        #     # FIXME: "Which is the noisiest, the most beautiful and the largest city?"
                        #     print('test 1')
                        # else:
                        #     print('test 2')

                        statement = Statement(sentence, target_chunk, action, related_chunk)
                        statements.append(statement)

        elif len(filtered_chunks) == 1:
            target_chunk = filtered_chunks[0]
            verb = get_verb_ancestor(target_chunk)
            action = _get_action(action_list, verb)
            first_word = target_chunk[0]

            # E.g.: "Which of the smart kids are famous?"
            # E.g.: "Who is very beautiful and very smart?"
            if not is_nsubj_wh_word(sentence, first_word) and action.acomp_list is not None:
                print('test 3')
                for acomp in action.acomp_list:
                    related_chunk = sentence[acomp.token.i: acomp.token.i + 1]
                    statement = Statement(sentence, target_chunk, action, related_chunk)
                    statements.append(statement)

    return statements


def _get_main_ancestor(chunk: Span):
    """
    Extract the noun ancestor if exists, otherwise the left edge item

    :param chunk: The current iterated chunk
    :return: The main ancestor
    """

    main_ancestor = get_noun_ancestor(chunk)

    if main_ancestor is None:
        main_ancestor = get_verb_ancestor(chunk)

        # E.g.: "When does the museum open?"
        if main_ancestor is None:
            main_ancestor = chunk.root.head
        main_ancestor = _get_left_edge(main_ancestor)

    return main_ancestor


def _get_action(action_list: [Span], word: Token):
    """
    TODO: pass the chunk => verb = get_verb_ancestor(related_chunk)
    Retrieve the event (Action) to which the word belongs

    :param action_list: The list of events (Actions)
    :param word: The input verb
    :return: The event (Action)
    """

    for action in action_list:
        verbs = action.verb.to_list()
        for verb in verbs:
            if verb == word:
                return action
    return None


def _get_associated_chunks(chunk_list, main_chunk):
    """
    Get the list of chunks which are in relation of conjunction with the main chunk

    :param chunk_list: The list of chunks in the sentence (see "get_noun_chunks")
    :param main_chunk: The current iterated chunk
    :return: The list of chunks which are in relation of conjunction with the main chunk
    """

    if main_chunk is None:
        return []

    # TODO: "Which is the noisiest, the most beautiful and the largest city?" => the most beautiful
    # E.g.: "Which is the noisiest and the largest city?"
    if len(main_chunk) == 1 and is_wh_noun_phrase(main_chunk):
        return [main_chunk]

    target_chunk_list = []
    conjuncts = [main_chunk.root] + list(main_chunk.conjuncts)

    for token in conjuncts:
        chunk = get_chunk(chunk_list, token)
        if chunk is not None:
            target_chunk_list.append(chunk)

    return target_chunk_list


def _get_left_edge(action_head):
    """
    Extract the left edge item which is not a verb

    :param action_head: The target head
    :return: The left edge item which is not a verb
    """

    left_edge = action_head.left_edge

    # 1. "How many days do I have to wait until the opening?"
    #   => action_head = "wait"
    #   => action_head.left_edge = "to"
    #   => action_head.left_edge.head.head = "have"
    # 2. "How many days do I have to wait until the opening?"
    if (left_edge.pos_ == "PART" and left_edge.tag_ == "TO" and left_edge.dep_ == "aux") or \
            (left_edge.pos_ == "ADP" and left_edge.tag_ == "IN" and left_edge.dep_ == "mark"):
        left_edge = left_edge.head.head

    if not is_verb(left_edge):
        return left_edge
    else:
        return _get_left_edge(action_head.head)
