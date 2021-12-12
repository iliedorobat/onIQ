from spacy.tokens import Doc, Span, Token
from iteration_utilities import unique_everseen

from ro.webdata.oniq.common.print_utils import echo

from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Statement import ConsolidatedStatement, Statement

from ro.webdata.oniq.nlp.actions import get_action_list, is_part_of_action
from ro.webdata.oniq.nlp.adj_utils import get_next_linked_adj_list, get_prev_linked_adj_list
from ro.webdata.oniq.nlp.chunk_utils import get_chunk_index, is_linked_chunk, get_noun_chunks
from ro.webdata.oniq.nlp.noun_utils import get_noun_ancestor, is_linked_noun
from ro.webdata.oniq.nlp.nlp_utils import extract_chunk, is_wh_noun_chunk, is_wh_noun_phrase, retokenize
from ro.webdata.oniq.nlp.phrase import prepare_phrase_list
from ro.webdata.oniq.nlp.utils import is_empty_list
from ro.webdata.oniq.nlp.verb_utils import get_verb_ancestor
from ro.webdata.oniq.nlp.word_utils import is_conjunction, is_preceded_by_conjunction, is_verb


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
    # FIXME: "How long is the journey?"
    chunk_list = get_noun_chunks(sentence)
    # Filter the chunks which are not in dependence of conjunction because they will be added
    # to target_chunks or related_chunks through the _get_associated_chunks method
    filtered_chunks = list(filter(lambda crr_chunk: _is_not_linked_to(crr_chunk), chunk_list))

    for chunk in filtered_chunks:
        main_ancestor = _get_main_ancestor(chunk)
        main_chunk = extract_chunk(filtered_chunks, main_ancestor)
        target_chunks = _get_target_chunks(chunk_list, main_chunk)

        if chunk != main_chunk:
            related_chunks = _get_associated_chunks(chunk_list, chunk)
            for target_chunk in target_chunks:
                for related_chunk in related_chunks:
                    if target_chunk != related_chunk:
                        verb = get_verb_ancestor(related_chunk)
                        action = _get_action(action_list, verb)
                        statements = _append_statement(statements, sentence, target_chunk, action, related_chunk)

        # E.g.: "Which is the noisiest and the largest city"
        # BUT NOT "Which is the noisiest town and the largest city"
        elif is_wh_noun_chunk(chunk) and len(filtered_chunks) == 1:
            related_chunks = _get_related_chunks(chunk_list, target_chunks)
            for target_chunk in target_chunks:
                verb = get_verb_ancestor(target_chunk)
                action = _get_action(action_list, verb)

                # E.g.: "Who is very smart?"
                # E.g.: "Who is very beautiful and very smart?"
                if len(related_chunks) == 0:
                    prev_adj_list = get_next_linked_adj_list(target_chunk)
                    statements = _append_adj_statement(prev_adj_list, statements, sentence, target_chunk, action)

                elif is_wh_noun_chunk(target_chunk) and action is not None:
                    for related_chunk in related_chunks:
                        statements = _append_statement(statements, sentence, target_chunk, action, related_chunk)
                        prev_adj_list = get_prev_linked_adj_list(related_chunk)
                        statements = _append_adj_statement(prev_adj_list, statements, sentence, target_chunk, action)

                    # Mirroring the list of statements as long as the list
                    # has been built from the end to the beginning
                    statements = statements[::-1]

        # E.g.: "Which of the smart kids are famous?"
        # E.g.: "Which woman is beautiful, generous, tall and rich?"
        elif len(filtered_chunks) == 1:
            for target_chunk in target_chunks:
                verb = get_verb_ancestor(target_chunk)
                action = _get_action(action_list, verb)
                next_linked_adj = get_next_linked_adj_list(target_chunk)
                statements = _append_adj_statement(next_linked_adj, statements, sentence, target_chunk, action)

        else:
            print("else...")
            pass

    return statements


# TODO: ilie.dorobat: add the documentation && add safety checks
def _append_adj_statement(adj_list: [Token], statements: [Statement], sentence: Span, target_chunk: Span, action: Action):
    for adj in adj_list:
        related_chunk = sentence[adj.token.i: adj.token.i + 1]
        statements = _append_statement(statements, sentence, target_chunk, action, related_chunk)

    return statements


# TODO: ilie.dorobat: add the documentation && add safety checks
def _append_statement(statements: [Statement], sentence: Span, target_chunk: Span, action: Action, related_chunk: Span):
    statement = Statement(sentence, target_chunk, action, related_chunk)
    statements.append(statement)
    return statements


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


def _is_not_linked_to(chunk: Span):
    """
    TODO: update the documentation
    TODO: ilie.dorobat: rename it to _is_linked_to
    Check if the root token is in relation of conjunction after the retokenization happened<br/>

    E.g.:
        - "Where can one find farhad and shirin monument?"
        - before retokenization, "farhad", "and", "shirin" were independent words
        - after retokenization, the "farhad and shirin" will be a named entity
        - after retokenization, the "monument" keeps its relation of conjunction, but,
                because the conjunction ("and") has been merged to a named entity, its
                relation is outdated

    :param chunk: The target chunk
    :return: True/False
    """

    if not isinstance(chunk, Span):
        return True

    if is_linked_chunk(chunk):
        for index, token in reversed(list(enumerate(chunk.sent[0: chunk[0].i]))):
            # E.g.: "Where can one find farhad and shirin monument?"
            if is_verb(token):
                return True
            # E.g.: "What museums are in Bacau, Iasi or Bucharest?"
            elif is_conjunction(token):
                return False

    return True


def _get_main_ancestor(chunk: Span):
    """
    Extract the noun ancestor if exists, otherwise the left edge item

    :param chunk: The current iterated chunk
    :return: The main ancestor
    """

    if not isinstance(chunk, Span):
        return None

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

    if is_empty_list(action_list) or not isinstance(word, Token):
        return None

    for action in action_list:
        verbs = action.verb.to_list()
        for verb in verbs:
            if verb == word:
                return action
    return None


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