from spacy.tokens import Doc, Span, Token
from iteration_utilities import unique_everseen

from ro.webdata.oniq.common.print_utils import echo

from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Adjective import Adjective
from ro.webdata.oniq.model.sentence.Statement import ConsolidatedStatement, Statement

from ro.webdata.oniq.nlp.actions import extract_action, get_action_list
from ro.webdata.oniq.nlp.adj_utils import get_next_linked_adj_list, get_prev_linked_adj_list
from ro.webdata.oniq.nlp.adv_utils import get_next_adv
from ro.webdata.oniq.nlp.chunk_utils import extract_chunk, get_chunk_index, get_filtered_noun_chunks, get_noun_chunks
from ro.webdata.oniq.nlp.noun_utils import get_noun_ancestor, is_linked_noun
from ro.webdata.oniq.nlp.nlp_utils import is_wh_noun_chunk, is_wh_noun_phrase, retokenize
from ro.webdata.oniq.nlp.phrase_utils import prepare_phrase_list
from ro.webdata.oniq.nlp.utils import is_empty_list
from ro.webdata.oniq.nlp.verb_utils import get_verb_ancestor
from ro.webdata.oniq.nlp.word_utils import is_preceded_by_conjunction, is_verb


def consolidate_statement_list(stmt_list: [Statement]):
    consolidated_list = []
    action = None

    if is_empty_list(stmt_list):
        return consolidated_list

    for i in range(0, len(stmt_list)):
        stmt = stmt_list[i]
        if i == 0:
            cons_stmt = ConsolidatedStatement(stmt)
            consolidated_list.append(cons_stmt)
        else:
            if action == stmt.action:
                last_cons_stmt = consolidated_list[len(consolidated_list) - 1]
                last_cons_stmt.related_phrases.append(stmt.related_phrase)
            else:
                cons_stmt = ConsolidatedStatement(stmt)
                consolidated_list.append(cons_stmt)
        action = stmt.action

    return consolidated_list


def get_statement_list(document: Doc):
    """
    Get the list of statements generated around the target phrases

    :param document: The parsed document
    :return: A list of statements
    """

    statements = []

    if not isinstance(document, Doc):
        return statements

    for sentence in document.sents:
        # retokenize(document, sentence)
        action_list = get_action_list(sentence)
        statements = _generate_statement_list(sentence, action_list)

        echo.token_list(sentence)
        echo.action_list(action_list)
        echo.statement_list(statements)

    return statements


# TODO: ilie.dorobat: add the documentation
def _generate_statement_list(sentence: Span, action_list: [Action]):
    statements = []

    if not isinstance(sentence, Span) or not isinstance(action_list, list):
        return statements

    # TODO: phrase_list = prepare_phrase_list(sentence) => instead of get_noun_chunks ???
    chunk_list = get_noun_chunks(sentence)
    filtered_chunks = get_filtered_noun_chunks(sentence)

    for index, chunk in enumerate(filtered_chunks):
        main_ancestor = _get_main_ancestor(filtered_chunks, index)
        main_chunk = extract_chunk(filtered_chunks, main_ancestor)
        target_chunks = _get_target_chunks(chunk_list, main_chunk)

        if chunk != main_chunk:
            related_chunks = _get_associated_chunks(chunk_list, chunk)
            for target_chunk in target_chunks:
                for related_chunk in related_chunks:
                    if target_chunk != related_chunk:
                        action = extract_action(action_list, related_chunk)
                        _append_statement(statements, target_chunk, action, related_chunk)

        # E.g.: "Which is the noisiest and the largest city"
        # BUT NOT "Which is the noisiest town and the largest city"
        elif is_wh_noun_chunk(chunk) and len(filtered_chunks) == 1:
            related_chunks = _get_related_chunks(chunk_list, target_chunks)
            for target_chunk in target_chunks:
                action = extract_action(action_list, target_chunk)

                # E.g.: "Who is very smart?"
                # E.g.: "Who is very beautiful and very smart?"
                if len(related_chunks) == 0:
                    prev_adj_list = get_next_linked_adj_list(target_chunk)
                    _append_adj_statements(sentence, statements, prev_adj_list, action, target_chunk)

                elif is_wh_noun_chunk(target_chunk) and action is not None:
                    for related_chunk in related_chunks:
                        _append_statement(statements, target_chunk, action, related_chunk)
                        prev_adj_list = get_prev_linked_adj_list(related_chunk)
                        _append_adj_statements(sentence, statements, prev_adj_list, action, target_chunk)

                    # Mirroring the list of statements as long as the list
                    # has been built from the end to the beginning
                    statements = statements[::-1]

        # E.g.: "Which of the smart kids are famous?"
        # E.g.: "Which woman is beautiful, generous, tall and rich?"
        # E.g.: "How many cars are there?"
        elif len(filtered_chunks) == 1:
            for target_chunk in target_chunks:
                action = extract_action(action_list, target_chunk)
                verb = get_verb_ancestor(target_chunk)
                next_adv = get_next_adv(verb)

                # E.g.: "How many cars are there?"
                if next_adv is not None:
                    _append_adv_statement(sentence, statements, target_chunk, action)
                else:
                    next_linked_adj = get_next_linked_adj_list(target_chunk)
                    _append_adj_statements(sentence, statements, next_linked_adj, action, target_chunk)

        else:
            print("else...")
            pass

    return statements


def _append_adj_statements(sentence: Span, statements: [Statement], adj_list: [Adjective], action: Action, target_chunk: Span):
    """
    Append new statements whose related chunk is built on an adjective

    E.g.:
        - question: "How long does the largest museum remain closed?"
        - question: "Which smart kid is famous?"

    :param sentence: The target sentence
    :param statements: The list of statements
    :param adj_list: The list of adjectives used to build the statements
    :param action: The target action
    :param target_chunk: The current target chunk (see _get_target_chunks)
    :return: None
    """

    if not isinstance(sentence, Span) or \
            not isinstance(statements, list) or \
            not isinstance(adj_list, list) or \
            not isinstance(action, Action) or \
            not isinstance(target_chunk, Span):
        return None

    for adj in adj_list:
        related_chunk = sentence[adj.token.i: adj.token.i + 1]
        _append_statement(statements, target_chunk, action, related_chunk)


def _append_adv_statement(sentence: Span, statements: [Statement], target_chunk: Span, action: Action):
    """
    Append a new statement whose related chunk is built on an adverb

    E.g.:
        - question: "How many cars are there?"

    :param sentence: The target sentence
    :param statements: The list of statements
    :param target_chunk: The current target chunk (see _get_target_chunks)
    :param action: The target action
    :return: None
    """

    if not isinstance(sentence, Span) or \
            not isinstance(statements, list) or \
            not isinstance(target_chunk, Span) or \
            not isinstance(action, Action):
        return None

    verb = get_verb_ancestor(target_chunk)
    adv = get_next_adv(verb)
    related_chunk = sentence[adv.token.i: adv.token.i + 1]
    _append_statement(statements, target_chunk, action, related_chunk)


def _append_statement(statements: [Statement], target_chunk: Span, action: Action, related_chunk: Span):
    """
    Append a new statement and update the previous one if the current statement
    phrase and/or related_phrase is in relation of conjunction

    :param statements: The list of statements
    :param target_chunk: The current target chunk (see _get_target_chunks)
    :param action: The target action
    :param related_chunk: The current related chunk (see _get_related_chunks)
    :return: None
    """

    if not isinstance(statements, list) or \
            not isinstance(target_chunk, Span) or \
            not isinstance(action, Action) or \
            not isinstance(related_chunk, Span):
        return None

    statement = Statement(target_chunk, action, related_chunk)
    _update_prev_statement(statements, statement)
    statements.append(statement)


def _update_prev_statement(statements: [Statement], statement: Statement):
    """
    Update the phrase and/or related_phrase of the previous statement based
    on the phrase and/or related_phrase of the input statement

    E.g.:
        - question: "How many paintings and statues are on display at the Amsterdam Museum?"
        - question: "What museums and libraries are in Bacau or Bucharest?"

    :param statements: The list of statements
    :param statement: The target statement
    :return: None
    """

    if is_empty_list(statements) or not isinstance(statement, Statement):
        return None

    prev_statement = statements[len(statements) - 1]
    if prev_statement is not None:
        if statement.phrase.conj is not None and prev_statement.phrase.prep_phrase is None:
            prev_statement.phrase.prep_phrase = statement.phrase.prep_phrase
        if statement.related_phrase.conj is not None and prev_statement.related_phrase.prep_phrase is None:
            prev_statement.related_phrase.prep_phrase = statement.related_phrase.prep_phrase


def _get_related_chunks(chunk_list: [Span], target_chunks: [Span]):
    related_chunks = []

    if is_empty_list(chunk_list) or is_empty_list(target_chunks):
        return related_chunks

    last_target_index = get_chunk_index(chunk_list, target_chunks[len(target_chunks) - 1])
    if len(chunk_list) > last_target_index:
        for index, related_chunk in enumerate(chunk_list):
            if index > last_target_index:
                last_word = related_chunk[len(related_chunk) - 1]
                if is_linked_noun(last_word):
                    related_chunks.append(related_chunk)
                else:
                    break

    return related_chunks


def _get_main_ancestor(filtered_chunks, index):
    """
    Extract the noun ancestor if exists, otherwise the left edge item

    :param filtered_chunks: The target chunks excluding the chunks which are in dependence of conjunction
    :param index: The index of the current iterated chunk
    :return: The main ancestor
    """

    chunk = filtered_chunks[index]
    if not isinstance(chunk, Span):
        return None

    main_ancestor = get_noun_ancestor(chunk)

    if main_ancestor is None:
        main_ancestor = get_verb_ancestor(chunk)

        # E.g.: "When does the museum open?"
        if main_ancestor is None:
            main_ancestor = chunk.root.head
        main_ancestor = _get_left_edge(main_ancestor)

    # E.g.: "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?"
    if main_ancestor is not None:
        main_ancestor = _get_prep_main_accessor(filtered_chunks, index, main_ancestor)

    return main_ancestor


# TODO: ilie.dorobat: add the documentation
def _get_prep_main_accessor(filtered_chunks, index, main_ancestor: Token):
    new_filtered_chunks = [chunk for idx, chunk in enumerate(filtered_chunks) if idx < index]
    found_chunk = extract_chunk(new_filtered_chunks, main_ancestor)

    # main_ancestor.i > 0   e.g.: "How long does the museum remain closed?"
    if found_chunk is None and main_ancestor.i > 0:
        return _get_prep_main_accessor(filtered_chunks, index, main_ancestor.head)

    return main_ancestor


# TODO: ilie.dorobat: add the documentation
def _get_target_chunks(chunk_list: [Span], main_chunk: Span):
    if not isinstance(main_chunk, Span):
        return []

    # E.g.: "Which is the noisiest and the largest city?"
    # E.g.: "Which is the noisiest, the most beautiful and the largest city?"
    if len(main_chunk) == 1 and is_wh_noun_phrase(main_chunk):
        return [main_chunk]

    # E.g.: "Which paintings, swords, coins or statues are in Bacau?"
    target_chunk_list = [main_chunk]

    if is_empty_list(chunk_list):
        return target_chunk_list

    for index, chunk in enumerate(chunk_list):
        noun_list = list(chunk.noun_chunks)
        if index > 0 and len(noun_list) > 0:
            if is_preceded_by_conjunction(noun_list[0][0]):
                target_chunk_list.append(chunk)
            else:
                break

    return target_chunk_list


def _get_associated_chunks(chunk_list: [Span], main_chunk: Span):
    """
    Get the list of chunks which are in relation of conjunction with the main chunk

    :param chunk_list: The list of chunks in the sentence (see "get_noun_chunks")
    :param main_chunk: The current iterated chunk
    :return: The list of chunks which are in relation of conjunction with the main chunk
    """

    if not isinstance(main_chunk, Span):
        return []

    # E.g.: "Which is the noisiest and the largest city?"
    # E.g.: "Which is the noisiest, the most beautiful and the largest city?"
    if len(main_chunk) == 1 and is_wh_noun_phrase(main_chunk):
        return [main_chunk]

    target_chunk_list = []
    conjuncts = [main_chunk.root] + list(main_chunk.conjuncts)

    for token in conjuncts:
        chunk = extract_chunk(chunk_list, token)
        if isinstance(chunk, Span):
            target_chunk_list.append(chunk)

    return target_chunk_list


def _get_left_edge(action_head):
    """
    Extract the left edge item which is not a verb

    :param action_head: The target head
    :return: The left edge item which is not a verb
    """

    if not isinstance(action_head, Token):
        return None

    left_edge = action_head.left_edge

    # 1. "How many days do I have to wait until the opening?"
    #   => action_head = "wait"
    #   => action_head.left_edge = "to"
    #   => action_head.left_edge.head.head = "have"
    # 2. "How many days do I have to wait until the opening?"
    if (left_edge.pos_ == "PART" and left_edge.tag_ == "TO" and left_edge.dep_ == "aux") or \
            (left_edge.pos_ == "ADP" and left_edge.tag_ == "IN" and left_edge.dep_ == "mark"):
        left_edge = left_edge.head.head

    # 1. "Did it rain most often at the beginning of the year?"
    if left_edge.i == 0 or not is_verb(left_edge):
        return left_edge
    else:
        return _get_left_edge(action_head.head)
